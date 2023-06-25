import os
import re
import pickle
import networkx as nx
import math
import matplotlib

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolBar, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

from src.loaders.asnr_dataloader import ASNRGraph
from src.static import PageState, GRAPH_VERSION_FOLDER, VERSIONS
from src.graph import Graph
# from .graph import GraphCanvas
from src.gui.social_graph.graph import GraphCanvas
from .modularity import Modularity

matplotlib.use("Qt5Agg")


class GraphEvolution(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.evolution_id = self.evolutions.index(PageState.version)  # Current evolution index

        # Background utilities
        self.graph_gui = GraphCanvas(parent)
        self.graph_gui_small = GraphCanvas(parent)
        self.info_tab = QLabel(text="Placeholder", alignment=Qt.AlignmentFlag.AlignCenter)
        self.info_tab2 = QLabel(text="Placeholder", alignment=Qt.AlignmentFlag.AlignCenter)

        # Load current graph information and replacing the placeholder
        self.refresh()

        # Building up graphical interface on generated information
        self.build_layout()

    # ===============================================
    # GUI build up
    # ===============================================

    def build_layout(self):
        # All layouts
        self.main_layout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.content_layout = QVBoxLayout()
        self.hlayout_below = QHBoxLayout()
        self.content_layout_below = QVBoxLayout()

        # Upper page: Left arrow + graph + right arrow
        self._create_prev_button()
        self.content_layout.addWidget(self.info_tab, 2)
        self.content_layout.addWidget(self.graph_gui, 8)
        self.hlayout.addLayout(self.content_layout)
        self._create_next_button()

        # Bottom page: Modularity + info tab + lower graph
        self.hlayout_below.addWidget(self.modularity.bar)
        self.content_layout_below.addWidget(self.info_tab2, 2)
        self.content_layout_below.addWidget(self.graph_gui_small, 8)
        self.hlayout_below.addLayout(self.content_layout_below)

        # Upper and bottom page added together
        self.main_layout.addLayout(self.hlayout)
        self.main_layout.addLayout(self.hlayout_below)
        self.setLayout(self.main_layout)

        # Disable buttons if first or last evolution indexed
        self._update_button_states()

    def _create_next_button(self):
        """Create a next button to this window"""
        self.next_button = QPushButton(QIcon("res/icons/right.png"), "", self)
        self.next_button.clicked.connect(self._next_button_on_click)
        size_hint = self.next_button.sizeHint()
        self.next_button.setFixedWidth(size_hint.width())
        self.hlayout.addWidget(self.next_button)

    def _create_prev_button(self):
        """Create a next button to this window"""
        self.prev_button = QPushButton(QIcon("res/icons/left.png"), "", self)
        self.prev_button.clicked.connect(self._prev_button_on_click)
        size_hint = self.prev_button.sizeHint()
        self.prev_button.setFixedWidth(size_hint.width())
        self.hlayout.addWidget(self.prev_button)

    # ===============================================
    # Properties
    # ===============================================

    @property
    def n_evolutions(self):
        """Number of evolutions"""
        return len(self.evolutions)

    @property
    def evolutions(self):
        """List of evolutions"""
        evolutions = VERSIONS[PageState.id]
        evolutions.sort()
        return evolutions

    @property
    def str_statistics(self):
        n_nodes = len(self.graph_gui.graph.nodes)
        n_edges = len(self.graph_gui.graph.directed_edges)
        avg_coeff = round(nx.average_clustering(G=self.graph_gui.graph.graph), 6)
        version = self.evolutions[self.evolution_id]
        return f"Version: {version} \n Number of nodes: {n_nodes}, " +\
               f"Number of edges: {n_edges} \n Average Clustering Coeffecient: {avg_coeff}"

    @property
    def str_modularity(self):
        return f"Community Visualization of {self.modularity.subcommunity_n} " + \
               f"communities with modularity of {self.modularity.max_modularity}"

    # ===============================================
    # Refresh on this page
    # ===============================================

    def refresh(self):
        """Refresh the page, the graph, the tabls, the buttons"""
        self._refresh_graph()
        self.info_tab.setText(self.str_statistics)
        self.info_tab2.setText(self.str_modularity)
        self._update_button_states()

    def _refresh_graph(self):
        """Refresh the graph"""
        version = self.evolutions[self.evolution_id]
        animal_folder = os.path.join(GRAPH_VERSION_FOLDER, PageState.id)

        # Load graphs
        if version != 'default' and os.path.exists(animal_folder) and os.listdir(animal_folder):
            file_path = os.path.join(GRAPH_VERSION_FOLDER, PageState.id, version + ".pkl")
            self.graph_gui.graph = Graph.from_pkl(filepath=file_path)
            self.graph_gui_small.graph = Graph.from_pkl(filepath=file_path)
        elif version == 'default':
            self.graph_gui.graph = Graph.from_graphml(PageState.graph_path)
            self.graph_gui_small.graph = Graph.from_graphml(PageState.graph_path)
        else:
            raise NameError(f"Version {version} does not exist")
        self.modularity = Modularity(self.graph_gui.graph.graph)
        self.graph_gui_small.node_colors = self.modularity.node_colors
        self.graph_gui.refresh()
        self.graph_gui_small.refresh()

    def _update_button_states(self):
        """Refresh the button states"""
        if hasattr(self, 'prev_button') and hasattr(self, 'next_button'):
            self.prev_button.setEnabled(self.evolution_id != 0)
            self.next_button.setEnabled(self.evolution_id != self.n_evolutions - 1)

    # ===============================================
    # Buttons trigger actions
    # ===============================================

    def _prev_button_on_click(self):
        """Jump back to previous evolution"""
        self.evolution_id = max(0, self.evolution_id - 1)
        self.refresh()

    def _next_button_on_click(self):
        """JUmp to next evolution"""
        self.evolution_id = min(self.n_evolutions - 1, self.evolution_id + 1)
        self.refresh()