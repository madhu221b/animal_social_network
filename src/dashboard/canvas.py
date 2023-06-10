import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from netgraph import InteractiveGraph
import networkx as nx

from utils.graph_utils import read_graph


DATASETS_PATH = os.getcwd().split("src")[0] + "/datasets" 

an2tex = {
  "Animal 1" :  os.path.join(DATASETS_PATH, "vampirebats_carter_mouth_licking_attribute_new.graphml")
}

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self,parent=None, width=5, height=4, dpi=100):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        graph, edge_color, node_color = read_graph(an2tex.get(parent.text)) # Handle Exception if animal is not in dataset
        self.mpl_connect('button_press_event', self.onclick)
        self.plot_instance = InteractiveGraph(graph, node_color=node_color, edge_color=edge_color, ax=self.ax)

    def onclick(self, event):
        if event.xdata is not None:
            node_name, node = self.get_closest_node(event.xdata, event.ydata)
            print("Node Name clicked: ", node_name)
        else:
            print("Clicked somewhere else..")  # access at event.x, event.y
    
    def get_closest_node(self, x, y):
        # Loop over all nodes, select the one closest to click
        closest_node = None
        distance = 999999
        closest_node_name = None
        for name in self.plot_instance.node_artists:
            node = self.plot_instance.node_artists[name]
            dist = ((x - node.xy[0])**2 + (y - node.xy[1])**2)**0.5
            if dist < distance:
                distance = dist
                closest_node = node
                closest_node_name = name
        return closest_node_name, closest_node

class Canvas(QMainWindow):
    def __init__(self, text=None, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.text = text
        self.canvas = MplCanvas(self,width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle(text)
        self.setGeometry(0, 0, 700, 700)

        layout = QtWidgets.QVBoxLayout(widget)
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)