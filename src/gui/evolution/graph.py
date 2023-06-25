# import networkx as nx
# import matplotlib
# from matplotlib import pyplot as plt
# import math
# from copy import deepcopy

# matplotlib.use("Qt5Agg")

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# from matplotlib.figure import Figure
# from netgraph import InteractiveGraph

# SHADES = plt.get_cmap("Pastel1")

# class GraphCanvas(FigureCanvasQTAgg):
#     """
#     Graph page, containing the graph and handling events such as clicks or hovers.
#     """

#     def __init__(self, parent=None, graph=None,node_layout=None, node_colors=None, width=5, height=4, dpi=100):
#         super(GraphCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
#         self.parent = parent
#         self.setParent(parent)
#         self.ax = self.figure.add_subplot(111)
#         self.nodecolors_2 = node_colors
#         # self.graph = graph
#         # self.degrees = self.get_degrees()
#         self.refresh(graph, node_layout)

#     def get_degrees(self):
#         return dict(self.graph.degree())

#     def min_degree(self):
#         return min(list(self.degrees.values()))

#     def max_degree(self):
#         return max(list(self.degrees.values()))

#     def node_colors(self):
#         norm = matplotlib.colors.Normalize(vmin=self.min_degree(),
#                                            vmax=self.max_degree(),
#                                            clip=True)

#         mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=SHADES)
#         colors = {}
#         for node, degree in self.degrees.items():
#             colors[node] = mapper.to_rgba(degree)
#         return colors

#     def edge_colors(self):
#         edge_colors = {}
#         for edge in self.graph.edges:
#             edge_colors[edge] = f"tab:gray"
#         return edge_colors

#     def refresh(self, graph, node_layout):
#         self.ax.cla()  # Clears the existing plot
#         self.graph = graph
#         self.degrees = self.get_degrees()
#         if node_layout is None:
#            pos = nx.spring_layout(graph, k=math.sqrt(1/ self.graph.order()))
#         else:
#             pos = node_layout

#         # if self.node_layout is not None:
#         #     for key, value in pos.items():
#         #         pos[key] = self.node_layout[key] if key in self.node_layout else value
#         node_color = None
#         if self.nodecolors_2:
#             node_color = self.nodecolors_2
#         else:
#             node_color = self.node_colors()
#         self.plot_instance = InteractiveGraph(graph,
#                                             node_color=node_color,
#                                              edge_color=self.edge_colors(),
#                                             #   node_edge_width=self.node_width,
#                                             #   node_shape=self.node_shapes,
#                                             #   node_size=self.node_sizes,
#                                             #   edge_width=self.edge_width,
#                                              node_layout=pos,
#                                               ax=self.ax)
