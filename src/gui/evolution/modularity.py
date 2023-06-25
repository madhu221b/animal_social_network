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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from mycolorpy import colorlist as mcp

cmap = plt.get_cmap("Pastel1")

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
        fig.subplots_adjust(top=0.4, left=0.2)

        fig.suptitle('Modularity for Different No. of Communities')
       
        rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))

        x_vals, y_vals = [], []
        for k in range(len(communities)):
            y_vals.append(nx.community.modularity(self.graph, communities[k]))
            x_vals.append(k+1)
        
        
        self.max_id = np.argmax(y_vals)
        self.max_modularity = round(np.max(y_vals),6)
        bar = ax.bar(x_vals, y_vals, color=cmap(rescale(y_vals)))
        ax.set_title("Modularity measures the density of connections within a community.", fontsize=6)
        ax.tick_params(axis='y', labelsize=6)
        ax.tick_params(axis='x', labelsize=6)
        ax.set_xlabel("No. of Communities",fontsize=6)
        ax.set_ylabel("Modularity Score",fontsize=6)
       

        fig.tight_layout(pad=4.0)   
        norm = matplotlib.colors.Normalize(vmin=min(y_vals), vmax=max(y_vals))
        ax2 = fig.add_axes([0.3 ,0.85, 0.4, 0.05])

        m_start = min(y_vals)         # colorbar min value
        m_end = max(y_vals)            # colorbar max value
        num_ticks = 3
        # to get ticks
        ticks = np.linspace(m_start, m_end, num_ticks)

        cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm,
        spacing='proportional', orientation='horizontal', ticks=ticks, format='%5f')   
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




        

        






