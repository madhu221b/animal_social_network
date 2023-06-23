from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import networkx as nx
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from mycolorpy import colorlist as mcp

class Modularity(QWidget):

    def __init__(self, graph):
        super(Modularity, self).__init__()

        self.max_id, self.max_modularity = -1, -1
        self.subcommunity_n = -1 
        self.graph = graph
        communities = list(nx.community.girvan_newman(self.graph))
        self.bar = self.get_bar(communities)
        if self.max_id != -1:
            community = communities[self.max_id]
            self.node_colors = self.create_community_node_colors(self.graph, community)


    
    def get_bar(self, communities):
        fig, ax  = plt.subplots()
        fig.suptitle('No. of Communities VS Modularity')
     

        x_vals, y_vals = [], []
        for k in range(len(communities)):
            y_vals.append(nx.community.modularity(self.graph, communities[k]))
            x_vals.append(k+1)
        
        
        self.max_id = np.argmax(y_vals)
        self.max_modularity = round(np.max(y_vals),6)
        ax.bar(x_vals, y_vals)
        ax.tick_params(axis='y', labelsize=5)
        ax.tick_params(axis='x')
        ax.set_xlabel("No. of Communities")
        ax.set_ylabel("Modularity Score")
        # ax.set_title("Modularity ax", fontsize=6)

        fig.tight_layout(pad=3.0)        
        return FigureCanvasQTAgg(fig)

    def create_community_node_colors(self,graph, community):
        number_of_colors = len(community)
        colors = mcp.gen_color(cmap="Pastel1", n=number_of_colors)

        node_colors = {}
        subcommunity_n = 0
        for i, subcommunity in enumerate(community):
            if len(subcommunity) != 0:
                subcommunity_n += 1
                for node in subcommunity:
                  node_colors[node] = colors[i]
        self.subcommunity_n = subcommunity_n
        return node_colors




        

        






