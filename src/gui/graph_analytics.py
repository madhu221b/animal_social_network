from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from collections import Counter
import networkx as nx
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts, dim

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
        self.graph = self.parent.graph_page.graph_page.graph
        self.edges_df = pd.DataFrame(self.graph.directed_edges, columns=['source', 'target'])
        self.graph_df = pd.merge(self.edges_df, self.features_df, left_on='source', right_on='node', how='left')
        self.graph_df = pd.merge(self.graph_df, self.features_df, left_on='target', right_on='node', how='left')

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

        chord_nodes = pd.DataFrame(columns=['name', 'group'])

        attribute_names = self.features_df.columns
        attribute_values = {}
        for column in self.features_df.columns:
            values = list(set(self.features_df[column].unique()))
            attribute_values[column] = values
            for value in values:
                chord_nodes.loc[len(chord_nodes)] = {'name': value, 'group': column}

        column_names = [str(column) + '_' + str(value) for column, values in attribute_values.items() for value in values]
        df = pd.DataFrame(0, index=column_names, columns=column_names)

        chord_df = pd.DataFrame(columns=['source', 'target', 'value'])
        for _, row in self.edges_df.iterrows():
            for att in attribute_names:
                source_value = self.features_df.loc[row['source']][att]
                target_value = self.features_df.loc[row['target']][att]
                df[att + '_' + str(source_value)][att + '_' + str(target_value)] += 1                
                if (chord_df[['source', 'target']] == [source_value, target_value]).all(axis=1).any():
                    condition = (chord_df['source'] == source_value) & (chord_df['target'] == target_value)
                    chord_df.loc[condition, 'value'] += 1
                else:
                    chord_df.loc[len(chord_df)] = {'source': source_value, 'target': target_value, 'value':1}

        hv.extension('matplotlib')
        opts.defaults(opts.Chord(cmap='Pastel1', edge_cmap='Pastel1', edge_color=dim('source').str(), node_color='index', labels='name'))

        chord = hv.Chord(chord_df)
        fig = hv.render(chord)

        # ax = fig.add_subplot(111)
        # ax.imshow(df.values)

        return FigureCanvasQTAgg(fig)