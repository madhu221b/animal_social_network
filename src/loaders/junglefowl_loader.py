from src.utils.graph_utils import read_graph, clean_nodes
from sklearn import preprocessing
import torch
import networkx as nx

def name_2_id(g):
    node_dict = {}
    i = 0
    for node, data in g.nodes(data=True):
        node_dict[node] = i
        i += 1
    return node_dict

def load_dataset(path, is_add_new_nodes=False):
    g,_,_ = read_graph(path,is_add_new_nodes)
    g = clean_nodes(g)     # 1. Remove unnecesary nodes
      
    node_dict = name_2_id(g) # 2. Map string names of animals to ids

    # 3. Encode the string names  by label encoders
    
    keys2val_str = {}
    for node, data in g.nodes(data=True):
        for key, val in data.items():
            if key not in keys2val_str:
                keys2val_str[key] = {}
                keys2val_str[key]["list"] = []
            keys2val_str[key]["list"].append(val)
    
        
     
    # 3.1 Declare Label Encoder objects
    for key, value in keys2val_str.items():
        le = preprocessing.LabelEncoder()
        list_of_vals = list(set(value["list"]))
        le.fit(list_of_vals)
        keys2val_str[key]["le"] = le


    ## 4. Collating node features ###
    nodes_size = len(node_dict)
    for node, data in g.nodes(data=True):
        feat_size = len([value for key, value in data.items()])
        break

    feat = torch.zeros(nodes_size, feat_size)

    i = 0
    for node, data in g.nodes(data=True):
        idx = node_dict[node]
        f = []
        for key, val in data.items():
            if isinstance(val, str):
                 le = keys2val_str[key]["le"]
                 f.append(le.transform([data[key]])[0])
            else:
                  f.append(val)
        f = torch.Tensor(f)
        feat[i] = f
        i += 1
        
    
    ## 5. Collating edge features ###
    edgelist = torch.zeros(g.number_of_edges(), 2)

    i = 0
    for u,v,data in g.edges(data=True):
        idx = node_dict[node]
        edgelist[i] = torch.Tensor([node_dict[u],node_dict[v]])
        i += 1
    adj =  nx.adjacency_matrix(g)

    features = {}
    for node, data in g.nodes(data=True):
        features[node] = data
    return feat, edgelist, adj, node_dict, features