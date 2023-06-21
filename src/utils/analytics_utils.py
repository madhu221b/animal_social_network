import networkx as nx
from collections import defaultdict
from scipy.stats import pearsonr

def get_correlations_att_edge(graph, features):
    ## Get correlation between difference in attributes and difference in edge weights

    # create the unweighted graph
    G = nx.Graph()
    G.add_nodes_from(graph.nodes())
    G.add_edges_from(graph.edges(), weight=1)

    # split string and number attributes
    # string_attributes = [features for n,_ in features.items() for attribute in features[n] if isinstance(features[n][attribute], str)]
    string_attributes = features.copy()
    number_attributes = features.copy()
    for n in string_attributes.keys():
        string_attributes[n] = {k: v for k, v in string_attributes[n].items() if isinstance(v, str)}
        number_attributes[n] = {k: v for k, v in number_attributes[n].items() if isinstance(v, (int, float))}

    

    # number_attributes = [features[n][attribute] for n,_ in features.items() for attribute in features[n] if isinstance(features[n][attribute], (int, float))]



    edges = list(G.edges())
    nodes = list(G.nodes())

    # get the closeness in attributes (1/diff)
    ivs = defaultdict(lambda: [])
    y = []

    node_pairs = [(n1, n2) for n1 in nodes for n2 in nodes if n1 != n2]
    for n1, n2 in node_pairs:
        attributes1 = string_attributes[n1]
        attributes2 = string_attributes[n2]
        for k in attributes1.keys():
            if attributes1[k] == attributes2[k]:
                ivs[k].append(1.)
            else:
                ivs[k].append(0.)
        
        attributes1 = number_attributes[n1] 
        attributes2 = number_attributes[n2] 
        for k in attributes1.keys():
            try: 
                ivs[k].append(1/(abs(attributes1[k] - attributes2[k]) + 1)) # +1 to avoid division by 0
            except KeyError: # temp fix TODO: fix this
                pass
        if G.has_edge(n1, n2):
            y.append(1)
        else:
            y.append(0)
            
    
    coeficcients = {}
    for k in ivs.keys():
        coeficcients[k] = pearsonr(ivs[k], y)

    return coeficcients





def get_correlation_att_att(graph, features):
    pass
