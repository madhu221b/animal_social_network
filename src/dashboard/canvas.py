import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolBar, QAction, QMessageBox
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
from src.dashboard.loaders.bat_loader import load_dataset

from src.dashboard.graph_analytics import GraphAnalytics

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
        self.metrics = metrics
        _, _, _, _, features = load_dataset(GRAPHS.get(parent.text))
        self.features = features
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
            self.parent.graph_page.right_page.update(node_name)

    def on_hover(self, event):

        if event.xdata is not None:
            node_name, node, is_hovering = self.get_closest_node(event.xdata, event.ydata)
            if is_hovering:
                # Mouse is over a node
                self.parent.graph_page.left_page.update(node_name)
            else:
                self.parent.graph_page.left_page.update("")
        else:
            self.parent.graph_page.left_page.update("")
    
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

        self.actions = {
            "add" : "add.png",
            "undo" : "undo.png",
            "open" : "open.png",
            "save" : "save.png"
        }

        self.parent = parent
        self._create_tool_bars()

        layout = QHBoxLayout()
        self.graph_page = GraphCanvas(parent, width=5, height=4, dpi=100)
        self.left_page = NodeInfoPage(self.graph_page.features,self.graph_page.metrics)
        self.right_page = NodeInfoPage(self.graph_page.features,self.graph_page.metrics)
        layout.addWidget(self.left_page)
        layout.addWidget(self.graph_page)
        layout.addWidget(self.right_page)
        self.setLayout(layout)

    def _create_tool_bars(self):
        self.toolbar = QToolBar(self.parent)
        self.parent.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        self.icon_actions = {}
        for action, img_filename in self.actions.items():
            self.icon_actions[action] = QAction(self)
            icon = QIcon(f"./res/icons/{img_filename}")
            self.icon_actions[action].setIcon(icon)
            self.icon_actions[action].setToolTip(action)  # Set tooltip to display action name on hover
            self.toolbar.addAction(self.icon_actions[action])

        # Connect the 'add' action to the _add_action method
        self.icon_actions['add'].triggered.connect(self._add_action)

    def _add_action(self):
        # Show a pop-up window when 'add' icon is clicked
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Add action was clicked!")
        msgBox.setWindowTitle("Add Action")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def _undo_action(self):
        pass

    def _delete_action(self):
        pass

    def _open_action(self):
        pass

    def _save_action(self):
        pass




class NodeInfoPage(QWidget):
    def __init__(self, features, metrics):
        super(NodeInfoPage, self).__init__()

        self.features = features
        self.metrics = metrics

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def update(self, node_name):
        while self.layout.count():
            item = self.layout.takeAt(0)            
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if not node_name:
            return

        title_label = QLabel('Features')
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.layout.addWidget(title_label)
        for feat in self.features[node_name]:
            if feat == 'population' or feat == 'Group' or feat == 'sex':
                feature_label = QLabel(f"{feat}: {self.features[node_name][feat]}")
                self.layout.addWidget(feature_label)

        title_label = QLabel('Metrics')
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.layout.addWidget(title_label)
        for key, value in self.metrics.items():
            metric_label = QLabel(f"{key}: {round(value[node_name], 2)}")
            self.layout.addWidget(metric_label)


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

        # Add pages
        tabs = QTabWidget()
        self.graph_page = GraphPage(self)
        self.graph_analytics = GraphAnalytics(self)
        tabs.addTab(self.graph_page, "Social Graph")
        tabs.addTab(self.graph_analytics, "Graph Analytics")
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
