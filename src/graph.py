from __future__ import annotations

import os
import logging
import pickle
import networkx as nx
from PyQt6.QtCore import QObject, pyqtSignal

from .static import PageState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('graph')


class Graph(QObject):

    node_selection_changed = pyqtSignal(list, name="node_change")
    edge_selection_changed = pyqtSignal(list, name="edge_change")

    # =====================================================
    # Initialisers
    # =====================================================

    def __init__(self, graph: nx.Graph):
        super().__init__()
        self.graph = graph
        self.deselect()
        self.clean_empty_nodes()
        self._selected_nodes = []
        self._selected_directed_edges = []
        self.fresh_nodes = []
        self.node_layout = None

    @classmethod
    def from_graphml(cls, filepath) -> Graph:
        logger.info(f"Reading graph {filepath}")
        graph_obj = cls(nx.read_graphml(filepath))
        return graph_obj

    @classmethod
    def from_state_dict(cls, state_dict) -> Graph:
        logger.info(f"Reading graph state_dict")
        graph_obj = cls(state_dict.pop('graph'))
        for key, value in state_dict.items():
            setattr(graph_obj, key, value)
        return graph_obj

    @classmethod
    def from_pkl(cls, filepath) -> Graph:
        logger.info(f"Reading graph {filepath}")
        with open(filepath, "rb") as f:
            state_dict = pickle.load(f)
        return cls.from_state_dict(state_dict)

    @classmethod
    def from_page_info(cls) -> Graph:
        if PageState.version.lower() == "default":
            return cls.from_graphml(PageState.graph_path)
        else:
            return cls.from_pkl(PageState.version_path)

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
    def unpredicted_new_node_names(self):
        degrees = self.degrees
        return [node for node in self.fresh_nodes if degrees[node] == 0]

    @property
    def predicted_new_node_names(self):
        degrees = self.degrees
        return [node for node in self.fresh_nodes if degrees[node] != 0]

    @property
    def selected_directed_edges(self):
        return self._selected_directed_edges

    @selected_nodes.setter
    def selected_nodes(self, value):
        self._selected_nodes = value
        self.node_selection_changed.emit(self._selected_nodes)

    @selected_directed_edges.setter
    def selected_directed_edges(self, value):
        self._selected_directed_edges = value
        self.edge_selection_changed.emit(self._selected_directed_edges)

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
        nodes = self.nodes
        return {nodes[node_name] for node_name in self.fresh_nodes if degrees[node_name] == 0}

    @property
    def predictable(self):
        # Can we run predict() on this graph
        return self.min_degree == 0

    @property
    def selected_undirected_edges(self):
        return [set([edge[0], edge[1]]) for edge in self.selected_directed_edges]

    @property
    def state_dict(self):
        return {"graph": self.graph, "node_layout": self.node_layout}

    # =====================================================
    # Add / remove nodes
    # =====================================================

    # Add

    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)
        # Note: append would not work here, because we need to trigger .setter
        self.selected_nodes = self._selected_nodes + [name for name, _ in nodes]
        self.fresh_nodes.extend([name for name, _ in nodes])
        logger.info(f"New nodes. Selected nodes are {self.selected_nodes}")

    def add_edges(self, edges):
        self.graph.add_edges_from(edges)
        # Note: append would not work here, because we need to trigger .setter
        self.selected_directed_edges = self._selected_directed_edges + list(edges)
        logger.info(f"New edges. Selected edges are {self.selected_directed_edges}")

    def add_node(self, node):
        self.add_nodes([node])

    def add_edge(self, edge):
        self.add_edges([edge])

    # Remove
    def remove_nodes(self, nodes=None):
        if nodes is None or nodes[0] is None:
            nodes = self.selected_nodes
        self.graph.remove_nodes_from(nodes)
        self.fresh_nodes = [n for n in self.fresh_nodes if n not in nodes]
        new_selection = [x for x in self.selected_nodes if x not in nodes]
        self.selected_nodes = new_selection

    def remove_edges(self, edges=None):
        if edges is None or edges[0] is None:
            edges = self.selected_directed_edges
        self.graph.remove_edges_from(self.selected_directed_edges)
        new_selection = [x for x in self.selected_directed_edges if x not in edges]
        self.selected_directed_edges = new_selection

    def remove_node(self, node=None):
        self.remove_nodes([node])

    def remove_edge(self, edge=None):
        self.remove_edges([edge])

    # =====================================================
    # Other utilities
    # =====================================================

    def toggle_status_of_node(self, node_name):
        if node_name in self.selected_nodes:
            logger.info(f"Node {node_name} unselected.")
            self._selected_nodes.remove(node_name)
        else:
            logger.info(f"Node {node_name} selected.")
            self._selected_nodes.append(node_name)
        self.node_selection_changed.emit(self._selected_nodes)
        logger.info(f"Selected nodes: {self.selected_nodes}")

    def toggle_status_of_edge(self, edge):
        if edge in self.selected_undirected_edges:
            if edge in self.selected_directed_edges:
                self._selected_directed_edges.remove(edge)
            else:
                self._selected_directed_edges.remove((edge[1], edge[0]))
            logger.info(f"Edge {edge} unselected.")
        else:
            self._selected_directed_edges.append(edge)
            logger.info(f"Edge {edge} selected.")
        self.edge_selection_changed.emit(self._selected_directed_edges)
        logger.info(f"Selected edges: {self.selected_directed_edges}")

    def edges_of(self, node):
        edges = []
        for edge in self.graph.edges:
            if edge[0] == node or edge[1] == node:
                edges.append(edge)
        return edges

    def select(self, nodes=None, edges=None):
        if nodes:
            if isinstance(nodes[0], tuple) or isinstance(nodes[0], list):
                self.selected_nodes = [name for name, _ in nodes]
            else:
                self.selected_nodes = nodes
        if edges:
            self.selected_directed_edges = edges

    def deselect(self):
        logger.info(f"Removed selection from everything.")
        self.selected_nodes = list()
        self.selected_directed_edges = list()

    def clean_empty_nodes(self):
        remove_arr = []
        for node, data in self.nodes:
            if len(data.keys()) == 0:
                remove_arr.append(node)
        [self.graph.remove_node(node) for node in remove_arr]
        return self.graph

    def reset(self):
        self.deselect()
        self.clean_empty_nodes()
        self.selected_nodes = []
        self.selected_directed_edges = []
        self.fresh_nodes = []
        # Note: layout stays