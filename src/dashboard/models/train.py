
"""
Usage :  python train.py --animal bat

"""
import numpy as np
import torch
from argparse import ArgumentParser

import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

import scipy.sparse as sp

from dashboard.canvas import an2tex
from dashboard.utils.gae_utils import mask_test_edges, preprocess_graph

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
n_epochs = 100
    
def get_preprocessed_adj(adj, features):
    # # Preprocess the data
    n_nodes, feat_dim = features.shape
    # Store original adjacency matrix (without diagonal entries) for later
    adj_orig = adj
    adj_orig = adj_orig - sp.dia_matrix((adj_orig.diagonal()[np.newaxis, :], [0]), shape=adj_orig.shape)
    adj_orig.eliminate_zeros()
    adj_train, train_edges, val_edges, val_edges_false, test_edges, test_edges_false = mask_test_edges(adj)
    adj = adj_train  
    
    # Some preprocessing
    adj_norm = preprocess_graph(adj)
    adj_label = adj_train + sp.eye(adj_train.shape[0])
    adj_label = torch.FloatTensor(adj_label.toarray())
    pos_weight = torch.Tensor([(adj.shape[0] * adj.shape[0] - adj.sum()) / adj.sum()])
    norm = adj.shape[0] * adj.shape[0] / float((adj.shape[0] * adj.shape[0] - adj.sum()) * 2)

    return features, adj_norm, adj_label, n_nodes, norm, pos_weight, adj_orig, val_edges, val_edges_false, test_edges, test_edges_false

def train_model(animal):
    path = an2tex[animal]
     
    if animal == "bat":
        from dashboard.loaders.bat_loader import load_dataset
        features, edgelist, adj, _= load_dataset(path)
        features, adj_norm, adj_label, n_nodes, norm, pos_weight, adj_orig, val_edges, val_edges_false, test_edges, test_edges_false = get_preprocessed_adj(adj, features)
            
        encoder = EncoderCora(input_feat_dim=feat_dim)
        decoder = DecoderCora()
        autoencoder = GraphAutoEncoderCora(encoder, decoder)
        encoder.to(device)
        decoder.to(device)

        # Train the Graph vae
        save_dir = Path.cwd() 

        if not save_dir.exists():
        os.makedirs(save_dir)


        autoencoder.fit(device, features,adj_norm, adj_label, n_nodes, norm, pos_weight,
        adj_orig,val_edges, val_edges_false, test_edges, test_edges_false, save_dir, n_epochs)


        autoencoder.load_state_dict(
        torch.load(save_dir / (autoencoder.name + ".pt")), strict=False
        )



if __name__ == '__main__':
    argp = ArgumentParser()

    argp.add_argument('--seed', default=0, type=int)
    argp.add_argument('--animal', default="bat")

    
    args = argp.parse_args()
    if args.seed:
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)

    train_model(args.animal)
    
    