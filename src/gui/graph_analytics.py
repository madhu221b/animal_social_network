from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from collections import Counter
import networkx as nx
import pandas as pd
import numpy as np

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

        self.node_features = self.parent.graph_page.graph_page.features
        self.features_df = pd.DataFrame(self.node_features).T
        self.features_df.index.name = 'node'

        self.setup_ui()

        
    def setup_ui(self):
        main_layout = QGridLayout(self)

        # Add attribute distribution plot
        attribute_distribution_plot = self.attribute_distribution_plot()
        main_layout.addWidget(attribute_distribution_plot, 0, 0, 1, 2)

        # Add adjacency matrix plot
        adj_matrix_plot = self.adjacency_matrix()
        main_layout.addWidget(adj_matrix_plot, 1, 0)

        # # Add chord diagram
        chord_diagram = self.chord_diagram()
        main_layout.addWidget(chord_diagram, 1, 1)


    def attribute_distribution_plot(self):
        plt.rcParams.update({'font.size': 8})
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.suptitle('Attribute Distribution')

        attribute_values = self.features_df.to_dict(orient='list')
        num_attributes = len(attribute_values)
        num_rows = num_attributes // 3 + num_attributes % 3 
        num_cols = 3 
        fig.subplots_adjust(hspace=5, wspace=0.3, left=0.08, right=0.98, top=0.93, bottom=0.15)

        for i, (attribute, values) in enumerate(attribute_values.items()):
            value_counts = Counter(values)
            values = list(value_counts.keys())
            count = list(value_counts.values())

            ax = fig.add_subplot(num_rows, num_cols, i+1)
            ax.barh(attribute, count[0], label=values[0], color=shades(0))
            for j in range(1, len(values)):
                ax.barh(attribute, count[j], left=sum(count[:j]), label=values[j], color=shades(j))

            ax.set_xlim(0, sum(count))
            ax.set_xticks(range(0, sum(count) + 1, 2))
            ax.set_xticklabels(range(0, sum(count) + 1, 2), fontsize=5)

            if len(values) > 8:
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -1.5), ncol=5, fontsize=4)
            else:
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -1.5), ncol=4, fontsize=5)
        
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
    

    def chord_diagram(self):
        fig = Figure(figsize=(3,3), dpi=100)

        return FigureCanvasQTAgg(fig)