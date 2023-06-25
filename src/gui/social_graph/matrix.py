
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
        fig = Figure(figsize=(6, 5), dpi=100)
        bi_adj_matrix = nx.adjacency_matrix(graph, weight=None)

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