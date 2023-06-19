"""
This file contains the modules of Graph VAE model.
The code from - https://github.com/zfjsail/gae-pytorch is adapted.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.module import Module
from torch.nn.parameter import Parameter
import torch.nn.modules.loss
from torch import optim

import os
import numpy as np
import pathlib
from pathlib import Path

import logging
import json
from src.utils.gae_utils import get_roc_score


def loss_function(preds, labels, mu, logvar, n_nodes, norm, pos_weight):
    cost = norm * F.binary_cross_entropy_with_logits(
        preds, labels, pos_weight=pos_weight
    )

    # see Appendix B from VAE paper:
    # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
    # https://arxiv.org/abs/1312.6114
    # 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    logvar = torch.nn.functional.normalize(logvar, dim=1)
    KLD = (
        -0.5
        / n_nodes
        * torch.mean(torch.sum(1 + 2 * logvar - mu.pow(2) - logvar.exp().pow(2), 1))
    )
    return cost + KLD


class GraphConvolution(Module):
    """
    Simple GCN layer, similar to https://arxiv.org/abs/1609.02907
    """

    def __init__(self, in_features, out_features, dropout=0.0, act=F.relu):
        super(GraphConvolution, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.dropout = dropout
        self.act = act
        self.weight = Parameter(torch.FloatTensor(in_features, out_features))
        self.reset_parameters()

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.weight)

    def forward(self, input, adj):
        input = F.dropout(input, self.dropout, self.training)
        support = torch.mm(input, self.weight)
        output = torch.spmm(adj, support)
        output = self.act(output)
        return output

    def __repr__(self):
        return (
            self.__class__.__name__
            + " ("
            + str(self.in_features)
            + " -> "
            + str(self.out_features)
            + ")"
        )


class Encoder(nn.Module):
    def __init__(self, input_feat_dim, hidden_dim1=4, hidden_dim2=4, dropout=0):
        super(Encoder, self).__init__()
        self.gc1 = GraphConvolution(input_feat_dim, hidden_dim1, dropout, act=F.relu)
        self.gc2 = GraphConvolution(hidden_dim1, hidden_dim2, dropout, act=lambda x: x)
        self.gc3 = GraphConvolution(hidden_dim1, hidden_dim2, dropout, act=lambda x: x)

    def forward(self, x, adj):
        hidden1 = self.gc1(x, adj)
        mu, logvar = self.gc2(hidden1, adj), self.gc3(hidden1, adj)
        return mu, logvar

    def mu(self, x, adj):
        mu = self.forward(x, adj)[0]
        return mu


class Decoder(nn.Module):
    """Decoder for using inner product for prediction."""

    def __init__(self, dropout=0, act=torch.sigmoid):
        super(Decoder, self).__init__()
        self.dropout = dropout
        self.act = act

    def forward(self, z):
        z = F.dropout(z, self.dropout, training=self.training)
        adj = self.act(torch.mm(z, z.t()))
        return adj


class GraphAutoEncoder(nn.Module):
    def __init__(
        self,
        encoder: Encoder,
        decoder: Decoder,
        name: str = "model",
        loss_f: callable = loss_function,
    ):
        """Class which defines model and forward pass.

        Parameters:
        ----------
        """
        super(GraphAutoEncoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.name = name
        self.loss_f = loss_f
        self.checkpoints_files = []
        self.lr = None

    def reparameterize(self, mu, logvar):
        """Samples from a normal distribution using the reparameterization trick.

        Parameters:
        -----------
        mean : torch.Tensor
            Mean of the normal distribution. Shape (batch_size, latent_dim)
        logvar : torch.Tensor
            Diagonal log variance of the normal distribution. Shape (batch_size,
            latent_dim)
        """
        if self.training:
            logvar = torch.nn.functional.normalize(logvar, dim=1)
            std = torch.exp(logvar)
            eps = torch.randn_like(std)
            return eps.mul(std).add_(mu)
        else:
            return mu

    def forward(self, x, adj):
        """Forward pass of model.

        Parameters:
        -----------
        x : torch.Tensor
            Batch of data. Shape (batch_size, n_chan, height, width)
        """
        mu, logvar = self.encoder(x, adj)
        z = self.reparameterize(mu, logvar)
        decode = self.decoder(z)
        return decode, mu, logvar

    def train_epoch(
        self,
        device: torch.device,
        train_loader_feats: torch.Tensor,
        train_loader_adj_norm: torch.Tensor,
        adj_label,
        n_nodes,
        norm,
        pos_weight,
        optimizer: torch.optim.Optimizer,
        scheduler,
    ) -> np.ndarray:
        train_loader_feats = train_loader_feats.to(device)
        train_loader_adj_norm = train_loader_adj_norm.to(device)
        adj_label = adj_label.to(device)
        pos_weight = pos_weight.to(device)
        self.train()
        optimizer.zero_grad()
        recovered, mu, logvar = self.forward(train_loader_feats, train_loader_adj_norm)
        loss = loss_function(
            preds=recovered,
            labels=adj_label,
            mu=mu,
            logvar=logvar,
            n_nodes=n_nodes,
            norm=norm,
            pos_weight=pos_weight,
        )
        loss.backward()
        cur_loss = loss.item()
        optimizer.step()
        # scheduler.step(loss)
        hidden_emb = mu.data.cpu().numpy()
        return hidden_emb, cur_loss

    def fit(
        self,
        device: torch.device,
        train_loader_feats: torch.Tensor,
        train_loader_adj_norm: torch.Tensor,
        adj_label,
        n_nodes,
        norm,
        pos_weight,
        adj_orig,
        val_edges,
        val_edges_false,
        test_edges,
        test_edges_false,
        animal,
        save_dir: pathlib.Path,
        n_epoch: int = 100,
        patience: int = 10,
        checkpoint_interval: int = -1,
    ) -> None:
        self.to(device)
        self.lr = 0.01
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode="min",
            factor=0.1,
            patience=10,
            threshold=0.0001,
            threshold_mode="abs",
        )
        waiting_epoch = 0
        for epoch in range(n_epoch):
            hidden_emb, train_loss = self.train_epoch(
                device,
                train_loader_feats,
                train_loader_adj_norm,
                adj_label,
                n_nodes,
                norm,
                pos_weight,
                optimizer,
                scheduler,
            )
            roc_curr, ap_curr = get_roc_score(
                hidden_emb, adj_orig, val_edges, val_edges_false
            )

            print(
                "Epoch:",
                "%04d" % (epoch + 1),
                "train_loss=",
                "{:.5f}".format(train_loss),
                "val_ap=",
                "{:.5f}".format(ap_curr),
            )

            if checkpoint_interval > 0 and epoch % checkpoint_interval == 0:
                n_checkpoint = 1 + epoch // checkpoint_interval
                print(f"Saving checkpoint {n_checkpoint} in {save_dir}")
                file = f"{save_dir}/{self.name}_{animal}_checkpoint{n_checkpoint}.pt"
                path_to_checkpoint = file
                torch.save(self.state_dict(), path_to_checkpoint)
                self.checkpoints_files.append(path_to_checkpoint)
            if waiting_epoch == patience:
                print("Early stopping activated")
                break
        print(f"Saving the model in {save_dir}")
        self.cpu()
        self.save(save_dir, animal)
        self.to(device)

        roc_score, ap_score = get_roc_score(
            hidden_emb, adj_orig, test_edges, test_edges_false
        )
        print(f"Test ROC score: {str(roc_score)}")
        print(f"Test AP score: {str(ap_score)}")

    def save(self, directory, animal) -> None:
        """Save a model and corresponding metadata.

        Parameters:
        -----------
        directory : pathlib.Path
            Path to the directory where to save the data.
        """
        model_name = self.name
        file_name = "{}_{}.pt".format(model_name, animal)
        path_to_model = os.path.join(directory, file_name)
        torch.save(self.state_dict(), path_to_model)
