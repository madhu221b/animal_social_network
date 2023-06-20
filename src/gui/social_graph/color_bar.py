from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHBoxLayout, QGridLayout
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import matplotlib as mpl
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')

mpl.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ColorBar(QWidget):

    def __init__(self, graph):
        super(ColorBar, self).__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.colorbar = self.get_colorbar(graph)
        self.layout.addWidget(self.colorbar, alignment=Qt.AlignmentFlag.AlignCenter)
    
        # self.layout.addStretch(1)
    

    def get_colorbar(self, graph):
    #    fig, ax = plt.subplots(figsize=(3, 100))
        # fig = Figure(figsize=(10, 1), dpi=100)
        # ax = fig.add_subplot(111)
        # fig, (ax, cax) = plt.subplots(figsize=(6, 1))
        fig, (ax, cax) = plt.subplots(1, 2)
        fig.subplots_adjust(bottom=0.15)
        degree = [val for (node, val) in graph.degree()]
        norm = mpl.colors.Normalize(vmin=min(degree), vmax=max(degree))
        # fig.subplots_adjust(hspace=5, wspace=0.3, left=0.08, right=0.98, top=0.93, bottom=0.15)
        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=shades),
             cax=cax, orientation='horizontal', label='Degree')
        return FigureCanvasQTAgg(fig)


    def refresh(self,graph):
        pass
        # n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
        # text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}, Type of interaction: "
        # self.info_tab.setText(text)


