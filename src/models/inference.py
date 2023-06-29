import os
import torch
import numpy as np
from src.models.gae import Encoder, Decoder, GraphAutoEncoder
from src.utils.gae_utils import preprocess_graph

from src.loaders.asnr_dataloader import ASNRGraph


def load_model(path, feat_dim):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    encoder = Encoder(input_feat_dim=feat_dim, hidden_dim1=32, hidden_dim2=16)
    decoder = Decoder()
    autoencoder = GraphAutoEncoder(encoder, decoder)
    encoder.to(device)
    decoder.to(device)

    model = autoencoder
    model.to(device)
    model.load_state_dict(torch.load(path))
    return model


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def get_pred_edges(graph, animal, version, new_name):
    save_dir = os.getcwd().split("src")[0] + "/results/models/"
    file_name = "model_{}_{}.pt".format(animal, version)
    path_to_model = os.path.join(save_dir, file_name)

    features, edgelist, adj, node_dict, _ = ASNRGraph(graph_obj=graph).preprocess()
    n_nodes, feat_dim = features.shape
    adj_norm = preprocess_graph(adj)
    model = load_model(path_to_model, feat_dim)
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    features = features.to(device)
    adj_norm = adj_norm.to(device)
    model.to(device)

    _, mu, logvar = model(features, adj_norm)
    mu = mu.data.cpu().numpy()
    adj_rec = np.dot(mu, mu.T)

    preds = torch.zeros(adj_rec.shape)
    for i, row_val in enumerate(adj_rec):
        for j, col_val in enumerate(adj_rec[i]):
            preds[i][j] = sigmoid(adj_rec[i][j])

    new_idx = 0
    for node, data in graph.nodes(data=True):
        if node == new_name:
            new_idx = node_dict[node]
            break

    src_name = [name for name, node_id in node_dict.items() if node_id == new_idx][0]
    new_edges = []
    for i, (pred, true) in enumerate(zip(preds[new_idx], adj_norm[new_idx])):
        if pred >= 0.5:
            name = [name for name, node_id in node_dict.items() if node_id == i][0]

            if name != src_name:
                new_edges.append((src_name, name))
        else:
            pass
    return new_edges
