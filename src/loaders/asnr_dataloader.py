from collections import defaultdict

import networkx as nx
import torch
import numpy as np
from sklearn import preprocessing

from matplotlib import cm, colors
import matplotlib.pyplot as plt

shades = plt.get_cmap("Pastel1")
random_state = np.random.RandomState(42)


def name_2_id(g):
    node_dict = {}
    i = 0
    for node, _ in g.nodes(data=True):
        node_dict[node] = i
        i += 1
    return node_dict


def clean_nodes(g):
    remove_arr = []
    for node, data in g.nodes(data=True):   
        if len(data.keys()) in  [0,1]:
            remove_arr.append(node) # Remove nodes with no keys or 1 key
        else:
            vals = data.values()
            if any(isinstance(val, str) and len(val.strip()) == 0 for val in vals):
                remove_arr.append(node) # Remove nodes with empty strings 
            elif any(isinstance(val, str) and val == "-" for val in vals):
                remove_arr.append(node) # some strings have useless spl char, "-"
            elif "tag_id" in data.keys():
                g.nodes[node].pop("tag_id",None)
                # g = g.remove_attribute(tnode=node, attr='tag_id')
            
    [g.remove_node(node) for node in remove_arr]
    return g


class ASNRGraph:
    def __init__(self, path=None, graph_obj=None) -> None:
        if graph_obj is None:
            self.graph = clean_nodes(nx.read_graphml(path))
        else:
            self.graph = graph_obj
        self.colors, self.centrality = self._init_colors()

    def _init_colors(self):
        g = self.graph
        edge_color, node_color = dict(), dict()

        for _, edge in enumerate(g.edges):
            edge_color[edge] = "tab:gray"

        minval = min([degree for _, degree in g.degree()])
        maxval = max([degree for _, degree in g.degree()])
        norm = colors.Normalize(vmin=minval, vmax=maxval, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=shades)

        for node, degree in g.degree():
            node_color[node] = mapper.to_rgba(degree)
        color_dict = {"node": node_color, "edge": edge_color}
        centrality_dict = {
            "betweeness": nx.betweenness_centrality(g),
            "closeness": nx.closeness_centrality(g),
            # "eigenvector": nx.eigenvector_centrality(g), # NOTE: Some graphs in the dataset don't converge and cause an error
            "degree": nx.degree_centrality(g),
        }
        return color_dict, centrality_dict

    def preprocess(self):
        node_dict = name_2_id(self.graph)

        # 3. Encode the string names  by label encoders
        keys2val_str = defaultdict(lambda: {"list": []})
        for node, data in self.graph.nodes(data=True):
            for key, val in data.items():
                keys2val_str[key]["list"].append(val)

        # 3.1 Declare Label Encoder objects
        for key, value in keys2val_str.items():
            le = preprocessing.LabelEncoder()
            list_of_vals = list(set(value["list"]))
            le.fit(list_of_vals)
            keys2val_str[key]["le"] = le

        # print(keys2val_str)
        ## 4. Collating node features ###
        nodes_size = len(node_dict)

        for node, data in self.graph.nodes(data=True):
            feat_size = len([value for _, value in data.items()])
            break

        feat = torch.zeros(nodes_size, feat_size)

        i = 0
        for node, data in self.graph.nodes(data=True):
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
        edgelist = torch.zeros(self.graph.number_of_edges(), 2)

        i = 0
        for u, v, data in self.graph.edges(data=True):
            edgelist[i] = torch.Tensor([node_dict[u], node_dict[v]])
            i += 1
        adj = nx.adjacency_matrix(self.graph)

        features = {}
        for node, data in self.graph.nodes(data=True):
            features[node] = data
        return feat, edgelist, adj, node_dict, features

    def graph(self):
        return self.graph, self.colors, self.centrality


if __name__ == "__main__":
    from glob import glob

    for file in glob("./datasets/**.graphml"):
        print(file)
        graph = ASNRGraph(file).preprocess()
        print("#########")
