
import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt6 import QtCore

shades = plt.get_cmap('cet_glasbey_light')
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import colorbar

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


def adjacency_matrix(graph):
        fig = Figure(figsize=(20, 15), dpi=100)
        bi_adj_matrix = nx.adjacency_matrix(graph, weight=None)

        ax = fig.add_subplot(111)
        # fig.suptitle('Adjacency Matrix', x=0.55)
        fig.tight_layout(pad=4.0)
        fig.subplots_adjust(top=0.95)

        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", "black"])
        im = ax.matshow(bi_adj_matrix.todense(), cmap='binary')
        nodes = list(graph.nodes)
        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes, fontsize=7)
        ax.set_yticklabels(nodes, fontsize=7)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

        ax.legend()
        # create a second axes for the colorbar
        bounds = [0, 1, 2]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        ax2 = fig.add_axes([0.85, 0.1, 0.03, 0.8])
        cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm,
        spacing='proportional', ticks=[0.5,1.5], boundaries=bounds, format='%1i')
        cb.set_ticklabels(['No Edge', 'Edge'])

        return fig