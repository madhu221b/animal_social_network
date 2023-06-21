from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHBoxLayout, QGridLayout
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import matplotlib as mpl
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')

mpl.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# TODO

class ColorBar(QWidget):

    def __init__(self, graph, ax, figure):
        super(ColorBar, self).__init__()
         
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.ax = ax
        self.figure = figure
        self.colorbar = self.get_colorbar(graph)
        self.layout.addWidget(self.colorbar)
    
        # self.layout.addStretch(1)
    

    def get_colorbar(self, graph):
        # fig, (ax, cax) = plt.subplots(1, 2)
        # fig.subplots_adjust(bottom=0.15)
        # degree = [val for (node, val) in graph.degree()]
        # norm = mpl.colors.Normalize(vmin=min(degree), vmax=max(degree))
        # fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=shades),
        #      cax=cax, orientation='horizontal', label='Degree')
        # fig, ax = plt.subplots(figsize=(1, 6))
        self.ax2 = self.figure.add_subplot(224)
        self.figure.subplots_adjust(bottom=0.5)

        # cmap = mpl.cm.cool
        # norm = mpl.colors.Normalize(vmin=5, vmax=10)

        # self.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        #             cax=self.ax2, orientation='horizontal', label='Some Units',shrink=1)
        degree = [val for (node, val) in graph.degree()]
        norm = mpl.colors.Normalize(vmin=min(degree), vmax=max(degree))
        self.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=shades),
              cax=self.ax2, orientation='horizontal', label='Degree')
        return FigureCanvasQTAgg(self.figure)


    def refresh(self,graph):
        pass
        # n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
        # text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}, Type of interaction: "
        # self.info_tab.setText(text)


