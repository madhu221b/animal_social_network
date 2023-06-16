import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from netgraph import InteractiveGraph

from src.utils.graph_utils import read_graph, get_edited_graph
from src.models.inference import get_pred_edges
from src.graph import Graph
from src.utils.common import seed_everything

SHADES = plt.get_cmap("Pastel1")


class GraphCanvas(FigureCanvasQTAgg):
    """
    Graph page, containing the graph and handling events such as clicks or hovers.
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(GraphCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.parent = parent
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)

        seed_everything(42)

        self.graph = Graph.from_file()
        self.mpl_connect('button_press_event', self.onclick)
        self.mpl_connect('motion_notify_event', self.on_hover)
        self.refresh()

    @property
    def features(self):
        return self.graph.features

    @property
    def metrics(self):
        return self.graph.metrics

    @property
    def node_colors(self):
        norm = matplotlib.colors.Normalize(vmin=self.graph.min_degree,
                                           vmax=self.graph.max_degree,
                                           clip=True)
        mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=SHADES)
        # return {node: mapper.to_rgba(degree) for (node, degree) in self.graph.degrees.items()}

        # Set the border color for selected nodes
        selected_border_color = "black"  # Change this to your desired border color
        selected_border_width = 2  # Change this to your desired border width

        colors = {}
        for node, degree in self.graph.degrees.items():
            if node in self.graph.selected_nodes:
                # Modify the node style for selected nodes
                color = mapper.to_rgba(degree)
                edge_color = selected_border_color
                edge_width = selected_border_width
            else:
                color = mapper.to_rgba(degree)
                edge_color = 'none'
                edge_width = 0

            colors[node] = {'node_color': color, 'edge_color': edge_color, 'edge_width': edge_width}
        return colors

    @property
    def edge_colors(self):
        edge_colors = {}
        for directed_edge in self.graph.directed_edges:
            undirected_edge = set(directed_edge)
            color = 'blue' if undirected_edge in self.graph.selected_undirected_edges else 'gray'
            edge_colors[directed_edge] = f"tab:{color}"
        return edge_colors

    def refresh(self):
        self.ax.cla()  # Clears the existing plot
        seed_everything(42)
        self.plot_instance = InteractiveGraph(self.graph.graph,
                                              node_color=self.node_colors,
                                              edge_color=self.edge_colors,
                                              ax=self.ax)

    def add_nodes(self, new_nodes, refresh=True):
        self.graph.add_nodes(new_nodes)
        if refresh:
            self.parent.graph_page.refresh()

    def add_node(self, new_node, refresh=True):
        self.add_nodes([new_node], refresh)

    def add_edges(self, new_edges, refresh=True):
        self.graph.add_edges(new_edges)
        if refresh:
            self.parent.graph_page.refresh()

    def add_edge(self, new_edge, refresh=True):
        self.add_edges([new_edge], refresh)

    def predict_edges(self, nodes=None, refresh=True):
        nodes = nodes if nodes else self.graph.selected_nodes
        pred_edges = []
        for node in nodes:
            pred_edges.extend(get_pred_edges(self.graph, self.parent.id, node))
        self.graph.add_edges(pred_edges)
        if refresh:
            self.parent.graph_page.refresh()

    def add_node_and_predict_edges(self, new_node):
        self.add_node(new_node, refresh=False)
        self.predict_edges(nodes=[new_node], refresh=True)

    def onclick(self, event):
        if event.xdata is not None:
            # Clicked on a node
            node_name, node, is_hovering = self.get_closest_node(event.xdata, event.ydata)
            if is_hovering:
                self.parent.graph_page.right_page.update(node_name, self.features, self.metrics)
                self.parent.graph_page.graph.toggle_status_of_node(node)
                self.parent.graph_page.refresh()

    def on_hover(self, event):

        if event.xdata is not None:
            node_name, _, is_hovering = self.get_closest_node(event.xdata, event.ydata)
        else:
            is_hovering = False

        if is_hovering:
            self.parent.graph_page.left_page.update(node_name, self.features, self.metrics)
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
