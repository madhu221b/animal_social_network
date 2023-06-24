import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
import math
from copy import deepcopy

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from netgraph import InteractiveGraph


SHADES = plt.get_cmap("Pastel1")


class GraphCanvas(FigureCanvasQTAgg):
    """
    Graph page, containing the graph and handling events such as clicks or hovers.
    """

    def __init__(self, parent=None, graph=None, width=5, height=4, dpi=100):
        super(GraphCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.parent = parent
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)

        # self.graph = graph
        # self.degrees = self.get_degrees()
        self.refresh(graph)
    
    def get_degrees(self):
        return dict(self.graph.degree())

    def min_degree(self):
        return min(list(self.degrees.values()))


    def max_degree(self):
        return max(list(self.degrees.values()))

    def node_colors(self):
        norm = matplotlib.colors.Normalize(vmin=self.min_degree(),
                                           vmax=self.max_degree(),
                                           clip=True)

        mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=SHADES)
        colors = {}
        for node, degree in self.degrees.items():
            colors[node] = mapper.to_rgba(degree)
        return colors
   
    def edge_colors(self):
        edge_colors = {}
        for edge in self.graph.edges:
            edge_colors[edge] = f"tab:gray"
        return edge_colors


    def refresh(self, graph):
        self.ax.cla()  # Clears the existing plot
        self.graph = graph
        self.degrees = self.get_degrees()
        pos = nx.spring_layout(graph, k=math.sqrt(12 / self.graph.order()))


        self.plot_instance = InteractiveGraph(graph,
                                            node_color=self.node_colors(),
                                             edge_color=self.edge_colors(),
                                            #   node_edge_width=self.node_width,
                                            #   node_shape=self.node_shapes,
                                            #   node_size=self.node_sizes,
                                            #   edge_width=self.edge_width,
                                             node_layout=pos,
                                              ax=self.ax)
        






