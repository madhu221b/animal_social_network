import networkx as nx
import numpy as np

from matplotlib import cm, colors
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')


random_state = np.random.RandomState(42)

def clean_nodes(g):
    remove_arr = []
    for node, data in g.nodes(data=True):
         if len(data.keys()) == 0:     
            remove_arr.append(node)
    [g.remove_node(node) for node in remove_arr]
    return g

def read_graph(path, is_add_new_nodes=False):
    g = nx.read_graphml(path)
    g = clean_nodes(g)
    
    edge_color, node_color = dict(), dict()

    
    for _, edge in enumerate(g.edges):
              edge_color[edge] = 'tab:gray' 
  
    
    minval = min([degree for _, degree in g.degree()])
    maxval = max([degree for _, degree in g.degree()])
    norm = colors.Normalize(vmin=minval, vmax=maxval, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=shades)
    
    for node, degree in g.degree():
        node_color[node] =  mapper.to_rgba(degree)
    color_dict = {"node":node_color, "edge":edge_color}
    centrality_dict = {"betweeness":nx.betweenness_centrality(g),
                       "closeness": nx.closeness_centrality(g),
                       "eigenvector": nx.eigenvector_centrality(g),
                       "degree": nx.degree_centrality(g)
    
                }
    return g, color_dict, centrality_dict

def get_edited_graph(g, new_node=None, new_edges=None):
        g = clean_nodes(g)
        
        edge_color, node_color = dict(), dict()

        if new_node:
            g.add_nodes_from([new_node])
        for _, edge in enumerate(g.edges):
                edge_color[edge] = 'tab:gray' 
            # else:
            #     edge_color[edge] = 'tab:blue' 
        
        minval = min([degree for _, degree in g.degree()])
        maxval = max([degree for _, degree in g.degree()])
        norm = colors.Normalize(vmin=minval, vmax=maxval, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=shades)
        
        for node, degree in g.degree():
            node_color[node] =  mapper.to_rgba(degree)
        color_dict = {"node":node_color, "edge":edge_color}
        centrality_dict = {"betweeness":nx.betweenness_centrality(g),
                        "closeness": nx.closeness_centrality(g),
                        "eigenvector": nx.eigenvector_centrality(g),
                        "degree": nx.degree_centrality(g)
        
                    }
        return g, color_dict, centrality_dict