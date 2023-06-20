from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel
import networkx as nx
import numpy as np

from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
class GraphAnalytics(QWidget):
    """
    Graph analytics page, contains metrics and visualizations
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # # Add GraphAnalytics canvas
        # graph_canvas = self.sampleplot()#GraphCanvas(self)
        # main_layout.addWidget(graph_canvas)

        # Add attribute distribution plot
        attribute_distribution_plot = self.attribute_distribution_plot()
        main_layout.addWidget(attribute_distribution_plot)

        # Add adjacency matrix plot
        adj_matrix_plot = self.adjacency_matrix()
        main_layout.addWidget(adj_matrix_plot)

    def sampleplot(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title('title')
        ax.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])

        return FigureCanvasQTAgg(fig)
    
    def adjacency_matrix(self):
        fig = Figure(figsize=(3,3), dpi=100)
        graph = self.parent.graph_page.graph_page.graph.graph
        adj_matrix = nx.adjacency_matrix(graph)
        ax = fig.add_subplot(111)
        ax.set_title('Adjacency Matrix')
        im = ax.matshow(adj_matrix.todense())
        nodes = list(graph.nodes)
        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes)
        ax.set_yticklabels(nodes)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

        fig.colorbar(im, ax=ax, label="Interaction Count")

        return FigureCanvasQTAgg(fig)

    def attribute_distribution_plot(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(121)
        ax.set_title('Attribute Distribution')
        node_features = self.parent.graph_page.graph_page.features
        attribute_names = sorted(set([key for _, value in node_features.items() for key, _ in value.items()]))

        attribute_counts = {}
        for att in attribute_names:
            attribute_counts[att] = []
        
        for features in node_features.values():
            for att in attribute_names:
                if att in features.keys():
                    attribute_counts[att].append(features[att])

        for attribute, counts in attribute_counts.items():
            element_counts = Counter(counts)
            values = list(element_counts.keys())
            count = list(element_counts.values())

            ax.barh(attribute, count[0], label=values[0], color=shades(0))
            for i in range(1, len(values)):
                ax.barh(attribute, count[i], left=sum(count[:i]), label=values[i], color=shades(i))
                ax.legend(loc='upper right', ncol=len(values),bbox_to_anchor=(2, 1.05))
        
        return FigureCanvasQTAgg(fig)