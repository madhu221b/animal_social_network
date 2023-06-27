import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6 import QtCore

shades = plt.get_cmap('Pastel2')
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import colorbar
from ..colors import cmap1
from ..custom_buttons import MediumGreenButton


class FullScreenWidget(QDialog):

    def __init__(self, graph, parent):
        super().__init__(parent)
        self.parent = parent
        self.graph = graph
        self.graph.graph_updated.connect(self.update_figure)

        self.setWindowTitle("Adjacency Matrix")
        self.setModal(True)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QVBoxLayout()

        self.button = MediumGreenButton("Close")
        self.button.clicked.connect(self.exit_fullscreen)
        self.layout.addWidget(self.button)

        self.update_figure()

        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.showMaximized()

    def exit_fullscreen(self):
        self.showNormal()
        self.close()

    def update_figure(self):
        # Clear the layout of figure
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, FigureCanvasQTAgg):
                self.layout.takeAt(i)
                widget.deleteLater()

        content_fig = self._adjacency_matrix(self.graph.graph)
        canvas = FigureCanvasQTAgg(content_fig)
        self.layout.insertWidget(0, canvas)

    def _adjacency_matrix(self, graph):
        fig = Figure(figsize=(20, 15), dpi=100)
        bi_adj_matrix = nx.adjacency_matrix(graph, weight=None)

        ax = fig.add_subplot(111)
        # fig.suptitle('Adjacency Matrix', x=0.55)
        fig.tight_layout(pad=4.0)
        fig.subplots_adjust(top=0.95)

        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ['white', cmap1(0.1)])
        im = ax.matshow(
            bi_adj_matrix.todense(),
            cmap=cmap,
        )

        nodes = list(graph.nodes)
        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes, fontsize=7)
        ax.set_yticklabels(nodes, fontsize=7)
        ax.set_xticks(np.arange(-.5, len(nodes), 1), minor=True)
        ax.set_yticks(np.arange(-.5, len(nodes), 1), minor=True)
        ax.grid(which='minor', color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

        ax.legend()
        # create a second axes for the colorbar
        bounds = [0, 1, 2]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        ax2 = fig.add_axes([0.85, 0.1, 0.03, 0.8])
        cb = matplotlib.colorbar.ColorbarBase(ax2,
                                              cmap=cmap,
                                              norm=norm,
                                              spacing='proportional',
                                              ticks=[0.5, 1.5],
                                              boundaries=bounds,
                                              format='%1i')
        cb.set_ticklabels(['No Edge', 'Edge'])

        return fig
