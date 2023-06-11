import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from netgraph import InteractiveGraph
import networkx as nx

from src.dashboard.utils.graph_utils import read_graph
from src.dashboard.slider import BSlider, CSlider

DATASETS_PATH = os.getcwd().split("src")[0] + "/datasets" 

GRAPHS = {
  "bat" :  os.path.join(DATASETS_PATH, "vampirebats_carter_mouth_licking_attribute_new.graphml")
}

class GraphCanvas(FigureCanvasQTAgg):
    """
    Graph page, containing the graph and handling events such as clicks or hovers.
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(GraphCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.parent = parent
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        graph, color, metrics = read_graph(GRAPHS.get(parent.text)) # Handle Exception if animal is not in dataset
        self.mpl_connect('button_press_event', self.onclick)
        self.mpl_connect('motion_notify_event', self.on_hover)
        self.plot_instance = InteractiveGraph(graph,
                                              node_color=color["node"],
                                              edge_color=color["edge"],
                                              ax=self.ax)

    def onclick(self, event):
        if event.xdata is not None:
            # Clicked on a node
            node_name, node, _ = self.get_closest_node(event.xdata, event.ydata)
            self.parent.graph_page.right_page.setText(node_name)

    def on_hover(self, event):

        if event.xdata is not None:
            node_name, node, is_hovering = self.get_closest_node(event.xdata, event.ydata)
            if is_hovering:
                # Mouse is over a node
                self.parent.graph_page.left_page.setText(node_name)
            else:
                self.parent.graph_page.left_page.setText("")
        else:
            self.parent.graph_page.left_page.setText("")
    
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
        return closest_node_name, closest_node, distance < closest_node.radius
class GraphPage(QWidget):
    """
    This is the page that belongs to the "graph" tab. It consists of three sub-pages:
     - Left page: shows information about the object which is hovered by the mouse
     - Graph page: shows the graph of animals
     - Right page: shows information about the selected object (the one last clicked on)
    """

    def __init__(self, parent):
        super().__init__()
        layout = QHBoxLayout()
        self.left_page = QLabel("Left")
        self.graph_page = GraphCanvas(parent, width=5, height=4, dpi=100)
        self.right_page = QLabel("Right")
        layout.addWidget(self.left_page)
        layout.addWidget(self.graph_page)
        layout.addWidget(self.right_page)
        self.setLayout(layout)
        

class MainCanvas(QMainWindow):
    """
    This is the main window, with tabs and 1 canvas (dashboard/page) for each tab.
    """

    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 700

    def __init__(self, text, *args, **kwargs):
        super(MainCanvas, self).__init__(*args, **kwargs)
        self.text = text
        self.setWindowTitle(text)
        self.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(widget)
        self.setLayout(self.layout)
        self.setCentralWidget(widget)

        # Menu
        tabs = QTabWidget()
        self.graph_page = GraphPage(self)
        tabs.addTab(self.graph_page, "Social Graph")
        # tabs.addTab(self.NodeUI(), "TO DO")
        self.layout.addWidget(tabs)
     
    # def _create_graph_page(self):
    #     """
    #      The Graph Visualization
    #     """
    #     tab = QWidget()
    #     layout = QHBoxLayout()

    #     self.graph_page = GraphCanvas(self, width=5, height=4, dpi=100)
        
    #     layout.addWidget(QLabel("Left"))
    #     layout.addWidget(self.graph_page)
    #     layout.addWidget(QLabel("Right"))
    #     tab.setLayout(layout)
    #     return tab
       
    # def NodeUI(self):
    #     generalTab = QWidget()
    #     layout = QVBoxLayout()
    #     self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
    #     self.toolbar = NavigationToolbar2QT(self.canvas, self)
    #     # layout.addWidget(self.toolbar)
    #     layout.addWidget(self.canvas)
    #     generalTab.setLayout(layout)
    #     return generalTab
       
    # def SliderUI(self):
    #     widget = QWidget()
    #     layout = QVBoxLayout()

    #     slider_b = BSlider(title="Betweenness Centrality")
    #     layout.addWidget(slider_b)

    #     slider_c = CSlider(title="Closeness Centrality")
    #     layout.addWidget(slider_c)
    #     widget.setLayout(layout)
    #     return widget