from __future__ import annotations

import networkx as nx
from PyQt5.QtCore import pyqtSignal

from .static import PageState


class Graph:

    node_selection_changed = pyqtSignal(object)
    edge_selection_changed = pyqtSignal(object)

    # =====================================================
    # Initialisers
    # =====================================================

    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.deselect()
        self.clean_empty_nodes()
        self._selected_nodes = []
        self._selected_directed_edges = []

    @classmethod
    def from_file(cls) -> Graph:
        return cls(nx.read_graphml(PageState.path))

    # =====================================================
    # Available features, metrics about the graph
    # =====================================================

    @property
    def centrality_dict(self) -> dict:
        return {
            "betweeness": nx.betweenness_centrality(self.graph),
            "closeness": nx.closeness_centrality(self.graph),
            "eigenvector": nx.eigenvector_centrality(self.graph),
            "degree": nx.degree_centrality(self.graph)
        }

    @property
    def selected_nodes(self):
        return self._selected_nodes

    @property
    def selected_directed_edges(self):
        return self._selected_nodes

    @selected_nodes.setter
    def selected_nodes(self, value):
        self._selected_nodes = value
        self.node_selection_changed.emit(len(self._selected_nodes))

    @selected_directed_edges.setter
    def selected_directed_edges(self, value):
        self._selected_directed_edges = value
        self.edge_selection_changed.emit(len(self._selected_directed_edges))

    @property
    def metrics(self) -> dict:
        return self.centrality_dict

    @property
    def nodes(self) -> dict:
        return self.graph.nodes(data=True)

    @property
    def features(self) -> dict:
        return dict(self.nodes)

    @property
    def directed_edges(self) -> dict:
        return self.graph.edges

    @property
    def undirected_edges(self) -> dict:
        return {k: set(v) for (k, v) in self.directed_edges.items()}

    @property
    def degrees(self):
        return dict(self.graph.degree())

    @property
    def min_degree(self):
        return min(list(self.degrees.values()))

    @property
    def max_degree(self):
        return max(list(self.degrees.values()))

    @property
    def hanging_nodes(self):
        degrees = self.degrees
        return {node: data for (node, data) in self.nodes if degrees[node] == 0}

    @property
    def predictable(self):
        # Can we run predict() on this graph
        return self.min_degree == 0

    @property
    def selected_undirected_edges(self):
        return [set(edge) for edge in self.selected_directed_edges]

    # =====================================================
    # Add / remove nodes
    # =====================================================

    # Add

    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)
        self.selected_nodes = list(nodes)

    def add_edges(self, edges):
        self.graph.add_edges_from(edges)
        self.selected_directed_edges = list(edges)

    def add_node(self, node):
        self.add_nodes([node])

    def add_edge(self, edge):
        self.add_edges([edge])

    # Remove

    def remove_nodes(self, nodes):
        self.graph.remove_nodes_from(nodes)
        self.selected_nodes = list(nodes)

    def remove_edges(self, edges):
        self.graph.remove_edges_from(edges)
        self.selected_directed_edges = list(edges)

    def remove_node(self, node):
        self.remove_nodes([node])

    def remove_edge(self, edge):
        self.remove_edges([edge])

    # =====================================================
    # Other utilities
    # =====================================================

    def toggle_status_of_node(self, node):
        if node in self.selected_nodes:
            self.selected_nodes.remove(node)
        else:
            self.selected_nodes.append(node)

    def toggle_status_of_edge(self, edge):
        if edge in self.selected_undirected_edges:
            if edge in self.selected_directed_edges:
                self.selected_directed_edges.remove(edge)
            else:
                self.selected_directed_edges.remove((edge[1], edge[0]))
        else:
            self.selected_directed_edges.append(edge)

    def edges_of(self, node):
        edges = []
        for edge in self.graph.edges:
            if edge[0] == node or edge[1] == node:
                edges.append(edge)
        return edges

    def select(self, nodes=None, edges=None):
        if nodes:
            self.selected_nodes = nodes
        if edges:
            self.selected_directed_edges = edges

    def deselect(self):
        self.selected_nodes = list()
        self.selected_directed_edges = list()

    def clean_empty_nodes(self):
        remove_arr = []
        for node, data in self.nodes:
            if len(data.keys()) == 0:
                remove_arr.append(node)
        [self.graph.remove_node(node) for node in remove_arr]
        return self.graph
