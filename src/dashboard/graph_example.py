"""
pip install pyqt5
pip install netgraph
"""

import sys

from PyQt5 import QtWidgets

import matplotlib

matplotlib.use("Qt5Agg")


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from netgraph import InteractiveGraph

import networkx as nx

graph_path = "/Users/madhurapawar/Documents/lab_assgs/mma/animalsocialnw_team7/datasets/vampirebats_carter_mouth_licking_attribute_new.graphml"

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        graph = nx.read_graphml(graph_path)
        self.plot_instance = InteractiveGraph(graph, ax=self.ax)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, text=None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)

        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()


if __name__ == "__main__":
    main()