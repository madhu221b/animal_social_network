from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHBoxLayout, QGridLayout
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import matplotlib as mpl
import matplotlib.pyplot as plt

# shades = plt.get_cmap('Pastel1')
from ..colors import cmap1

mpl.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ColorBar(FigureCanvasQTAgg):

    def __init__(self, parent, graph, width=5, height=1, dpi=100):
        super().__init__(Figure(figsize=(width, height), dpi=dpi))
        self.parent = parent
        self.setParent(parent)

        # Numbers are: left-margin, bottom-margin, width, height
        self.ax = self.figure.add_axes([0.05, 0.5, 0.9, 0.1])

        degree = [val for (node, val) in graph.degree()]
        norm = mpl.colors.Normalize(vmin=min(degree), vmax=max(degree))
        self.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap1),
                             cax=self.ax,
                             orientation='horizontal',
                             label='Degree')