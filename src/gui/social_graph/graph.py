import os
import matplotlib

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from netgraph import InteractiveGraph
import networkx as nx

from src.utils.graph_utils import read_graph, get_edited_graph
from src.models.inference import get_pred_edges

DATASETS_PATH = os.getcwd().split("src")[0] + "/datasets"

GRAPHS = {
    "bat": os.path.join(DATASETS_PATH, "vampirebats_carter_mouth_licking_attribute_new.graphml"),
    "junglefowl": os.path.join(DATASETS_PATH, "junglefowl_mcdonald_sexual_network_group9_attribute.graphml") 
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
        graph, pos, color, metrics = read_graph(GRAPHS.get(parent.text)) # Handle Exception if animal is not in dataset
        self.graph = graph
        self.metrics = metrics
        self.features = {node:data for node,data in self.graph.nodes(data=True)}
        self.mpl_connect('button_press_event', self.onclick)
        self.mpl_connect('motion_notify_event', self.on_hover)
        self.plot_instance = InteractiveGraph(graph,
                                              node_color=color["node"],
                                              node_layout = pos,
                                              edge_color=color["edge"],
                                              ax=self.ax)
    

    def update_graph(self, new_node=None, new_edges=None):
        if new_node: # infer new edges
            new_graph, pos, _ , _ = get_edited_graph(self.graph, new_node=new_node)
            pred_edges = get_pred_edges(new_graph, self.parent.text, new_node[0])

            graph, pos, color, metrics = get_edited_graph(new_graph, new_node=new_node, new_edges=pred_edges)
            self.graph = graph
            self.metrics = metrics
            self.features = {node:data for node,data in self.graph.nodes(data=True)}


        self.ax.cla() # Clears the existing plot
        self.plot_instance = InteractiveGraph(self.graph,
                                              node_color=color["node"],
                                              node_layout = pos,
                                              edge_color=color["edge"],
                                              ax=self.ax)
        
    def onclick(self, event):
        if event.xdata is not None:
            # Clicked on a node
            node_name, node, _ = self.get_closest_node(event.xdata, event.ydata)
            self.parent.graph_page.right_page.update(node_name, self.features, self.metrics)

    def on_hover(self, event):

        if event.xdata is not None:
            node_name, node, is_hovering = self.get_closest_node(event.xdata, event.ydata)
            if is_hovering:
                # Mouse is over a node
                self.parent.graph_page.left_page.update(node_name, self.features, self.metrics)
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
