from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QPushButton, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QTableWidget
import networkx as nx
import numpy as np
from ..utils.analytics_utils import get_correlations_att_edge

from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

shades = plt.get_cmap('Set3')

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class FullScreenWidget(QDialog):

    def __init__(self, content_fig, parent):
        super().__init__(parent)
        self.parent = parent

        self.setWindowTitle("Adjacency Matrix")
        self.setModal(True)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        canvas = FigureCanvasQTAgg(content_fig)
        self.layout = QVBoxLayout()
        self.layout.addWidget(canvas)

        self.button = QPushButton("Close", self)
        self.button.clicked.connect(self.exit_fullscreen)
        self.button.setStyleSheet("font-size: 24px; padding 10px;")
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.showMaximized()

    def exit_fullscreen(self):
        self.showNormal()
        self.close()


class GraphAnalytics(QWidget):
    """
    Graph analytics page, contains metrics and visualizations
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)

        # Create a vertical layout for the plots
        self.plots_layout = QVBoxLayout()
        plots_layout = self.plots_layout

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        node_features = self.parent.graph_page.graph_page.features
        disc_attribute_labels = sorted([
            k for k, v in list(node_features.values())[0].items() if type(v) == str or int(v) == v
        ],
                                       key=lambda x: x.lower())
        cont_attribute_labels = sorted([
            k for k,
            v in list(node_features.values())[0].items() if type(v) == float and int(v) != v
        ],
                                       key=lambda x: x.lower())

        # Add discrete attribute distribution plot
        if len(disc_attribute_labels) > 0:
            attribute_distribution_plot = self.attribute_distribution_plot()
            attribute_distribution_plot.setFixedHeight(40*len(disc_attribute_labels))
            plots_layout.addWidget(attribute_distribution_plot)

        # Add attribute distribution plot continuous variables
        # Note, I made some attempts at adding the scroll bar, but it didn't work out
        if len(cont_attribute_labels) > 0:

            attribute_distribution_cont = self.attribute_distribution_cont()
            attribute_distribution_cont.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                                      QtWidgets.QSizePolicy.Policy.Expanding)
            attribute_distribution_cont.setFixedHeight(100*len(cont_attribute_labels))
            plots_layout.addWidget(attribute_distribution_cont)

        adj_matrix_plot = self.adjacency_matrix()
        fullscreen_widget = FullScreenWidget(adj_matrix_plot, self)

        # Add adjacency matrix plot

        # self.adj_canvas = FigureCanvasQTAgg(adj_matrix_plot)
        # plots_layout.addWidget(self.adj_canvas)
        # self.adj_canvas.mpl_connect("button_press_event", lambda event: fullscreen_widget.showMaximized())

        # # Add heatmap
        try:
            heatmap_plot = self.heatmap()
            heatmap_plot.setFixedHeight(500)
            plots_layout.addWidget(heatmap_plot)
        except:
            pass

        plots_layout.addStretch()
        plots_widget = QWidget()
        plots_widget.setLayout(plots_layout)
        scroll.setWidget(plots_widget)
        container_layout.addWidget(scroll)

        # Add the plots layout to the container layout
        # container_layout.addLayout(plots_layout)

        table_layout = QVBoxLayout()
        # Add graph analytics table
        graph_analytics_table = self.graph_analytics_table()
        table_layout.addWidget(graph_analytics_table)

        button = QPushButton("Adjacency Matrix", self)
        button.clicked.connect(fullscreen_widget.show)
        button.setStyleSheet("font-size: 24px; padding 10px;")
        table_layout.addWidget(button)

        container_layout.addLayout(table_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container_widget)

    def adjacency_matrix(self):
        fig = Figure(figsize=(8, 5), dpi=100)
        graph = self.parent.graph_page.graph_page.graph.graph
        bi_adj_matrix = nx.adjacency_matrix(graph, weight=None)
        # adj_matrix = nx.adjacency_matrix(graph, weight='weight')

        ax = fig.add_subplot(111)
        fig.suptitle('Adjacency Matrix', x=0.55)
        fig.tight_layout(pad=3.0)
        im = ax.matshow(bi_adj_matrix.todense(), cmap='binary')
        nodes = list(graph.nodes)
        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes)
        ax.set_yticklabels(nodes)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

        ax.legend()
        cbar = fig.colorbar(im, ax=ax, cmap='binary', ticks=[0, 1], shrink=0.5)
        cbar.set_ticklabels(['No Edge', 'Edge'])

        # canvas = FigureCanvasQTAgg(fig)
        return fig

    def heatmap(self):
        graph = self.parent.graph_page.graph_page.graph.graph
        node_features = self.parent.graph_page.graph_page.features
        correlations = get_correlations_att_edge(graph, node_features)
        fig = Figure(figsize=(7, 5), dpi=100)
        fig.suptitle('Correlation between attributes and edge existence')
        fig.text(
            0.5,
            0.04,
            "Pearson\'s two-tailed correlation coefficients between the existence of an edge between nodes, and similarity between the two nodes in various attributes. * indicates p<0.05 with Bonferroni correction.",
            ha='center',
            fontsize=8,
            wrap=True)
        ax = fig.add_subplot(111)
        attributes = list(correlations.keys())
        # delete nan values
        for i in reversed(range(len(attributes))):
            if np.isnan(correlations[attributes[i]][0]):
                del correlations[attributes[i]]
                del attributes[i]

        coefficients = [c[0] for c in list(correlations.values())]
        p_values = [c[1] for c in list(correlations.values())]
        array = np.array(coefficients).reshape(1, len(correlations))
        im = ax.imshow(array, cmap='seismic', vmin=-0.5, vmax=0.5)

        #add legend
        fig.colorbar(im,
                     ax=ax,
                     label="Correlation",
                     cmap='seismic',
                     ticks=[0.5, 0, -0.5],
                     shrink=0.5)

        ax.set_xticks(np.arange(len(attributes)), labels=attributes)
        plt.setp(ax.get_xticklabels(), rotation=80, ha="right", rotation_mode="anchor")

        # remove yticks
        ax.set_yticks([])
        for i in range(len(attributes)):
            # ax.text(i,
            #         -0.25,
            #         str(round(coefficients[i], 2)),
            #         ha='center',
            #         va='center',
            #         color='black',
            #         fontsize=8)
            if p_values[i] < 0.05 / len(attributes):  # bonferroni correction
                ax.text(i, 0.25, '*', ha='center', va='center', color='black', fontsize=8)

        return FigureCanvasQTAgg(fig)

    def graph_analytics_table(self):
        graph = self.parent.graph_page.graph_page.graph.graph
        n = graph.number_of_nodes()
        graph_metrics = {
            'Number of Nodes':
                graph.number_of_nodes(),
            'Number of Edges':
                graph.number_of_edges(),
            'Density':
                round(nx.density(graph), 3),
            'Diameter':
                nx.diameter(graph),
            'Average Degree':
                round(sum([d for _, d in graph.degree()]) / n, 3),
            'Average Clustering':
                round(nx.average_clustering(graph), 3),
            'Average Shortest Path':
                round(nx.average_shortest_path_length(graph), 3),
            'Average Betweenness Centrality':
                round(sum([b for _, b in nx.betweenness_centrality(graph).items()]) / n, 3),
            'Average Closeness Centrality':
                round(sum([c for _, c in nx.closeness_centrality(graph).items()]) / n, 3),
            'Average Eigenvector Centrality':
                round(sum([e for _, e in nx.eigenvector_centrality(graph).items()]) / n, 3),
            'Average PageRank':
                round(sum([p for _, p in nx.pagerank(graph).items()]) / n, 3),
            'Average Degree Centrality':
                round(sum([d for _, d in nx.degree_centrality(graph).items()]) / n, 3)
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

    def attribute_distribution_cont(self):
        fig = Figure(figsize=(7, 5), dpi=100)
        node_features = self.parent.graph_page.graph_page.features
        attribute_labels = sorted([
            k for k,
            v in list(node_features.values())[0].items() if type(v) == float and int(v) != v
        ],
                                  key=lambda x: x.lower())
        n = len(attribute_labels)
        fig.suptitle('Node Attribute Distribution (continuous variables)')
        fig.text(0.5,0.5, s="test")
        fig.tight_layout(pad=0.5)
        c = 2
        k = int(np.ceil(n / c))
        for i in range(n):
            ax = fig.add_subplot(k, c, i + 1)  # Need to make scrollable
            attribute = attribute_labels[i]
            attribute_values = [
                features[attribute]
                for features in node_features.values()
                if attribute in features.keys()
            ]
            ax.bar(np.arange(len(attribute_values)), attribute_values, width=0.5)
            ax.tick_params(axis='y', labelsize=5)
            ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax.set_title(attribute, fontsize=6)

        # fig.tight_layout(pad=3.0)
        return FigureCanvasQTAgg(fig)

    def attribute_distribution_plot(self):
        fig = Figure(figsize=(6, 5), dpi=100)
        node_features = self.parent.graph_page.graph_page.features
        attribute_labels = sorted([
            k for k, v in list(node_features.values())[0].items() if type(v) == str or int(v) == v
        ],
                                  key=lambda x: x.lower())
        # attribute_labels = sorted(set([key for _, value in node_features.items() for key, v in value.items() if type(v) == str or int(v) == v]), key=lambda x: x.lower())
        n = len(attribute_labels)
        fig.suptitle("Node Attribute Distribution")
        fig.tight_layout(pad=3.0)
        bars = []
        for i in range(n):
            ax = fig.add_subplot(n, 1, i + 1)
            attribute = attribute_labels[i]
            attribute_values = [
                features[attribute]
                for features in node_features.values()
                if attribute in features.keys()
            ]
            element_counts = Counter(attribute_values)
            values = list(element_counts.keys())
            count = list(element_counts.values())

            for i in range(len(values)):
                bar = ax.barh(attribute,
                              count[i],
                              left=sum(count[:i]),
                              label=values[i],
                              color=shades(i))
                bars.extend(bar)
                ax.text(sum(count[:i]) + count[i] / 2,
                        attribute,
                        str(count[i]),
                        ha='center',
                        va='center',
                        color="white",
                        alpha=0.5,
                        fontsize=8,
                        fontweight='bold')
            ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

            # for bar in bars:
            #     bar.set_picker(True)

        def onclick(event):
            ax_save = None
            for bar in bars:
                if bar.contains(event)[0]:
                    ax = bar.axes
                    l = ax.legend(bbox_to_anchor=(0.8, 0.7), loc='best')
                    # set zorder
                    l.set_zorder(200)
                    # fig.canvas.draw_idle()
                    ax_save = ax
                    break

            # This seems like a round-about way, but is necessary since mulitple bars are part of the same axes
            for bar in bars:
                ax = bar.axes
                if ax != ax_save:
                    ax.legend().remove()

            fig.canvas.draw_idle()

        fig.canvas.mpl_connect("button_press_event", onclick)

        return FigureCanvasQTAgg(fig)
