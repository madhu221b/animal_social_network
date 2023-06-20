from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QTableWidget
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
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)

        # Create a vertical layout for the plots
        plots_layout = QVBoxLayout()
        
        # Add attribute distribution plot
        attribute_distribution_plot = self.attribute_distribution_plot()
        plots_layout.addWidget(attribute_distribution_plot)

        # Add adjacency matrix plot
        adj_matrix_plot = self.adjacency_matrix()
        plots_layout.addWidget(adj_matrix_plot)

        # Add the plots layout to the container layout
        container_layout.addLayout(plots_layout)

        # Add graph analytics table
        graph_analytics_table = self.graph_analytics_table()
        container_layout.addWidget(graph_analytics_table)

        scroll_area.setWidget(container_widget)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)


        # Add descriptive table
    def graph_analytics_table(self):
        graph = self.parent.graph_page.graph_page.graph.graph
        n = graph.number_of_nodes()
        graph_metrics = {
            'Number of Nodes': graph.number_of_nodes(),
            'Number of Edges': graph.number_of_edges(),
            'Density': round(nx.density(graph), 3),
            'Diameter': nx.diameter(graph),
            'Average Degree': round(sum([d for _, d in graph.degree()]) / n,3),
            'Average Clustering': round(nx.average_clustering(graph), 3),
            'Average Shortest Path': round(nx.average_shortest_path_length(graph), 3),
            'Average Betweenness Centrality': round(sum([b for _, b in nx.betweenness_centrality(graph).items()]) / n,3),
            'Average Closeness Centrality': round(sum([c for _, c in nx.closeness_centrality(graph).items()]) / n,3),
            'Average Eigenvector Centrality': round(sum([e for _, e in nx.eigenvector_centrality(graph).items()]) / n,3),
            'Average PageRank': round(sum([p for _, p in nx.pagerank(graph).items()]) / n,3),
            'Average Degree Centrality': round(sum([d for _, d in nx.degree_centrality(graph).items()]) / n,3)
         }
        table = QTableWidget()
        table.setRowCount(len(graph_metrics))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Metric', 'Value'])
        # table.setVerticalHeaderLabels(graph_metrics.keys())
        for i, (metric, value) in enumerate(graph_metrics.items()):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(metric))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        return table



    
    def update_ui(self):
        self.setup_ui()

    def adjacency_matrix(self):
        fig = Figure(figsize=(6,5), dpi=100)
        graph = self.parent.graph_page.graph_page.graph.graph
        bi_adj_matrix = nx.adjacency_matrix(graph, weight=None)
        # adj_matrix = nx.adjacency_matrix(graph, weight='weight')

        ax = fig.add_subplot(111)
        ax.set_title('Binary Adjacency Matrix')
        im = ax.matshow(bi_adj_matrix.todense())
        nodes = list(graph.nodes)
        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes)
        ax.set_yticklabels(nodes)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
        fig.colorbar(im, ax=ax, label="Edge Existence")

        # ax = fig.add_subplot(122)
        # ax.set_title('Adjacency Matrix')
        # im = ax.matshow(adj_matrix.todense())
        # nodes = list(graph.nodes)
        # ax.set_xticks(np.arange(len(nodes)))
        # ax.set_yticks(np.arange(len(nodes)))
        # ax.set_xticklabels(nodes)
        # ax.set_yticklabels(nodes)
        # plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
        # fig.colorbar(im, ax=ax, label="Interaction Count")


        return FigureCanvasQTAgg(fig)

    def attribute_distribution_plot(self):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
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
                # ax.legend(loc='upper right', ncol=len(values),bbox_to_anchor=(2, 1.05))
        
        return FigureCanvasQTAgg(fig)