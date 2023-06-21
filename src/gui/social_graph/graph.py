import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
import math
from copy import deepcopy

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from netgraph import InteractiveGraph

from src.utils.graph_utils import read_graph, get_edited_graph
from src.models.inference import get_pred_edges
from src.graph import Graph

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

        self.graph = Graph.from_page_info()
        self.mpl_connect('button_release_event', self.onclick)
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
        colors = {}
        for node, degree in self.graph.degrees.items():
            colors[node] = mapper.to_rgba(degree)
        return colors

    @property
    def node_sizes(self):
        sizes = {}
        predicted = self.graph.predicted_new_node_names
        unpredicted = self.graph.unpredicted_new_node_names
        for node_name, _ in self.graph.nodes:
            if node_name in predicted:
                sizes[node_name] = 5
            elif node_name in unpredicted:
                sizes[node_name] = 6
            else:
                sizes[node_name] = 3
        return sizes

    @property
    def node_shapes(self):
        shapes = {}
        predicted = self.graph.predicted_new_node_names
        unpredicted = self.graph.unpredicted_new_node_names
        for node_name, _ in self.graph.nodes:
            if node_name in predicted:
                shapes[node_name] = "s"
            elif node_name in unpredicted:
                shapes[node_name] = "^"
            else:
                shapes[node_name] = "o"
        return shapes

    @property
    def edge_colors(self):
        edge_colors = {}
        for directed_edge in self.graph.directed_edges:
            undirected_edge = set(directed_edge)
            color = 'blue' if undirected_edge in self.graph.selected_undirected_edges else 'gray'
            edge_colors[directed_edge] = f"tab:{color}"
        return edge_colors

    @property
    def node_width(self):
        width = {}
        for node_name, node in self.graph.nodes:
            width[node_name] = 1. if node_name in self.graph.selected_nodes else 0.5
        return width

    @property
    def edge_width(self):
        width = {}
        for edge in self.graph.directed_edges:
            undirected_edge = set(edge)
            width[edge] = 1.5 if undirected_edge in self.graph.selected_undirected_edges else 1.
        return width

    def refresh(self):
        self.ax.cla()  # Clears the existing plot
        pos = nx.spring_layout(self.graph.graph, k=math.sqrt(1 / self.graph.graph.order()))

        if self.graph.node_layout is not None:
            for key, value in pos.items():
                pos[key] = self.graph.node_layout[key] if key in self.graph.node_layout else value

        self.plot_instance = InteractiveGraph(self.graph.graph,
                                              node_color=self.node_colors,
                                              edge_color=self.edge_colors,
                                              node_edge_width=self.node_width,
                                              node_shape=self.node_shapes,
                                              node_size=self.node_sizes,
                                              edge_width=self.edge_width,
                                              node_layout=pos,
                                              ax=self.ax)
        self.graph.node_layout = deepcopy(self.plot_instance.node_positions)

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
        if refresh:
            self.parent.graph_page.refresh()

    def remove_nodes(self, new_nodes, refresh=True):
        self.graph.remove_nodes(new_nodes)
        if refresh:
            self.parent.graph_page.refresh()

    def remove_node(self, new_node, refresh=True):
        self.remove_nodes([new_node], refresh)

    def remove_edges(self, new_edges, refresh=True):
        self.graph.remove_edges(new_edges)
        if refresh:
            self.parent.graph_page.refresh()

    def remove_edge(self, new_edge, refresh=True):
        self.remove_edges([new_edge], refresh)
        if refresh:
            self.parent.graph_page.refresh()

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
            node_name, _, is_hovering, was_dragged = self.get_closest_node(event.xdata, event.ydata)
            if is_hovering and not was_dragged:
                # Click
                self.parent.graph_page.right_page.update(node_name, self.features, self.metrics)
                self.parent.graph_page.graph_page.graph.toggle_status_of_node(node_name)
                self.parent.graph_page.refresh()
            elif is_hovering and was_dragged:
                self.graph.node_layout[node_name] = self.plot_instance.node_positions[node_name]
            else:
                self.graph.deselect()
                self.parent.graph_page.refresh()
        else:
            self.graph.deselect()
            self.parent.graph_page.refresh()

    def on_hover(self, event):

        if event.xdata is not None:
            node_name, _, is_hovering, _ = self.get_closest_node(event.xdata, event.ydata)
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

        hovering = distance < closest_node.radius
        was_dragged = False
        if hovering and hasattr(self,
                                "plot_instance") and not isinstance(self.graph.node_layout, str):
            was = tuple(self.graph.node_layout[closest_node_name])
            now = tuple(self.plot_instance.node_positions[closest_node_name])
            was_dragged = not was == now

        return closest_node_name, closest_node, hovering, was_dragged
