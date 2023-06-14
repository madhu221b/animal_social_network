from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel

class GraphAnalytics(FigureCanvasQTAgg):
    """
    Graph analytics page, contains metrics and visualisations
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(GraphAnalytics, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.parent = parent
        self.setParent(parent)
        self.ax = self.figure.add_subplot(211)
        self.node_features = self.parent.graph_page.graph_page.features

        attribute_names = set([key for _, value in self.node_features.items() for key, _ in value.items()])

        attribute_counts = {}
        for att in attribute_names:
            attribute_counts[att] = []
        
        for features in self.node_features.values():
            for att in attribute_names:
                if att in features.keys():
                    attribute_counts[att].append(features[att])

        for attribute, counts in attribute_counts.items():
            element_counts = Counter(counts)
            values = list(element_counts.keys())
            count = list(element_counts.values())

            self.ax.barh(attribute, count[0], label=values[0], color=shades(0))
            self.ax.legend(loc='upper center', ncol=len(values), bbox_to_anchor=(0.5, -0.15))
            for i in range(1, len(values)):
                self.ax.barh(attribute, count[i], left=sum(count[:i]), label=values[i], color=shades(i))