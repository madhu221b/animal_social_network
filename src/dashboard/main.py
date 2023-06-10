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

graph_path = "datasets/vampirebats_carter_mouth_licking_attribute_new.graphml"


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.mpl_connect('button_press_event', self.onclick)
        graph = nx.read_graphml(graph_path)
        self.plot_instance = InteractiveGraph(graph, ax=self.ax)

    def onclick(self, event):
        if event.xdata is not None:
            node_name, node = self.get_closest_node(event.xdata, event.ydata)
            print(node_name)
        else:
            print("Clicked somewhere else..")  # access at event.x, event.y

    def get_closest_node(self, x, y):
        # Loop over all nodes, select the one closest to click
        closest_node = None
        distance = 999999
        cosest_node_name = None
        for name in self.plot_instance.node_artists:
            node = self.plot_instance.node_artists[name]
            dist = ((x - node.xy[0])**2 + (y - node.xy[1])**2)**0.5
            if dist < distance:
                distance = dist
                closest_node = node
                cosest_node_name = name
        return cosest_node_name, closest_node


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
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
