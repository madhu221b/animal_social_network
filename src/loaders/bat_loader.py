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

def load_dataset(path=None, graph=None, is_add_new_nodes=False):

    if graph is None:
        g,_,_,_ = read_graph(path,is_add_new_nodes)
    else:
        g = graph
    g = clean_nodes(g)     # 1. Remove unnecesary nodes
      
    node_dict = name_2_id(g) # 2. Map string names of animals to ids

    # 3. Encode the string names and phenotypes by label encoders
    
    population = set()
    group = set()
    gender = set()
    genes = set()
    for node, data in g.nodes(data=True):
        data_val = [value for key, value in data.items()]
        population.add(data_val[0])
        group.add(data_val[1])
        gender.add(data_val[2])
        genes.update(data_val[3:])
        
    population, group, gender, genes = list(population), list(group), list(gender), list(genes)   
    # 3.1 Declare Label Encoder objects
    pe = preprocessing.LabelEncoder()
    pe.fit(population)

    gp = preprocessing.LabelEncoder()
    gp.fit(group)

    gd = preprocessing.LabelEncoder()
    gd.fit(gender)

    gn = preprocessing.LabelEncoder()
    gn.fit(genes)

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
        f.append(pe.transform([data["population"]])[0])
        f.append(gp.transform([data["Group"]])[0])
        f.append(gd.transform([data["sex"]])[0])
        genes = [value for key, value in data.items()][3:]
        f.extend(gn.transform(genes))
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