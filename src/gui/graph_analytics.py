from collections import Counter
import networkx as nx
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout


class GraphAnalytics(QWidget):
    def __init__(self, parent=None):
        super(GraphAnalytics, self).__init__(parent)
        self.parent = parent
        self.setParent(parent)
        self.layout = QGridLayout(self)
        self.heatmap = Heatmap(self)
        self.chord_diagram = ChordDiagram(self)
        self.bar_chart = BarChart(self)
        self.layout.addWidget(self.bar_chart, 0, 0, 1, 2)
        self.layout.addWidget(self.heatmap, 1, 0)
        self.layout.addWidget(self.chord_diagram, 1, 1)
        self.setLayout(self.layout)

        self.node_features = self.parent.graph_page.graph_page.features
        self.graph = self.parent.graph_page.graph_page.graph
        self.features_df = pd.DataFrame(self.node_features).T
        self.features_df.index.name = 'node'
        self.edges_df = pd.DataFrame(nx.to_pandas_edgelist(self.graph), columns=['source', 'target'])
        self.graph_df = pd.merge(self.edges_df, self.features_df, left_on='source', right_on='node', how='left')
        self.graph_df = pd.merge(self.graph_df, self.features_df, left_on='target', right_on='node', how='left')

        self.bar_chart.display_bar_chart()

        attribute_names = self.features_df.columns
        attribute_values = {}
        for column in self.features_df.columns:
            attribute_values[column] = list(set(self.features_df[column].unique()))

        column_names = [(column, value) for column, values in attribute_values.items() for value in values]
        df = pd.DataFrame(0, index=pd.MultiIndex.from_tuples(column_names),
                          columns=pd.MultiIndex.from_tuples(column_names))

        for _, row in self.edges_df.iterrows():
            for att in attribute_names:
                source_value = self.features_df.loc[row['source']][att]
                target_value = self.features_df.loc[row['target']][att]
                df[(att, source_value)][(att, target_value)] += 1
        

class Heatmap(QWidget):
    def __init__(self, parent=None):
        super(Heatmap, self).__init__(parent)
        self.parent = parent
        self.layout = QGridLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas, 0, 0)
        self.setLayout(self.layout)


class ChordDiagram(QWidget):
    def __init__(self, parent=None):
        super(ChordDiagram, self).__init__(parent)
        self.parent = parent
        self.layout = QGridLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas, 0, 0)
        self.setLayout(self.layout)


class BarChart(QWidget):
    def __init__(self, parent=None):
        super(BarChart, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    
    def display_bar_chart(self):
        attribute_values = self.parent.features_df.to_dict(orient='list')
        num_attributes = len(attribute_values)
        num_rows = num_attributes // 3 + num_attributes % 3 
        num_cols = 3 
        self.figure.subplots_adjust(hspace=7, left=0.05, right=0.95, top=0.95, bottom=0.15)

        for i, (attribute, values) in enumerate(attribute_values.items()):
            value_counts = Counter(values)
            values = list(value_counts.keys())
            count = list(value_counts.values())

            ax = self.figure.add_subplot(num_rows, num_cols, i+1)
            ax.barh(attribute, count[0], label=values[0], color=shades(0))
            for j in range(1, len(values)):
                ax.barh(attribute, count[j], left=sum(count[:j]), label=values[j], color=shades(j))

            ax.set_xlim(0, sum(count))
            ax.set_xticks(range(0, sum(count) + 1, 2))
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -1.25), ncol=4)

        self.canvas.draw()