import os
import re
import pickle
import networkx as nx
import matplotlib

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolBar, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from src.loaders.asnr_dataloader import ASNRGraph
from src.static import PageState, GRAPH_VERSION_FOLDER
from .graph import GraphCanvas

matplotlib.use("Qt5Agg")
class GraphEvolution(QWidget):
    """
    This is the page that belongs to the "graph" tab. It consists of three sub-pages:
     - Left page: shows information about the object which is hovered by the mouse
     - Graph page: shows the graph of animals
     - Right page: shows information about the selected object (the one last clicked on)
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        

        # Page
        self.main_layout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.content_layout = QVBoxLayout()
        

        self.current_graph_id = PageState.version
        self.animal = PageState.id
        self.linked_list = self.get_linked_list(self.animal)  
        self.graph_obj = self.linked_list[self.current_graph_id]["graph"]
        n_nodes, n_edges = self.graph_obj.number_of_nodes(), self.graph_obj.number_of_edges()
        self.text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}"

        self.graph = GraphCanvas(parent, graph=self.graph_obj, width=5, height=4, dpi=100)
        self.info_tab = QLabel(text=self.text, alignment=Qt.AlignmentFlag.AlignCenter)
        
         # Add content
        self.content_layout.addWidget(self.graph, 8)
        self.content_layout.addWidget(self.info_tab, 2)

        self._create_prev_button()
        self.hlayout.addLayout(self.content_layout)
        self._create_next_button()

        
        self.main_layout.addLayout(self.hlayout)
        # self.main_layout.addWidget(self.info_tab)
        
        self.setLayout(self.main_layout)

    def get_linked_list(self, animal):
        linked_list = dict()
        animal_folder = os.path.join(GRAPH_VERSION_FOLDER, animal)
        for file_name in os.listdir(animal_folder):
            result = re.compile("(v)\d+(.)").search(file_name)
            if result:
                id = result.group(0).replace(".","")
                file_path = os.path.join(animal_folder, file_name)
                with open(file_path, "rb") as f:
                     state_dict = pickle.load(f)
                linked_list[id] = state_dict
        
        asnr = ASNRGraph(path=PageState.graph_path)
        linked_list["default"] = {"graph": asnr.graph, "prev":-1}
        linked_list[self.current_graph_id]["next"] = -1
        
        # updating next ids
        curr_id = self.current_graph_id
        while True:     
            prev_id = linked_list[curr_id]["prev"]
            if prev_id == -1: break # reached the end
        
            linked_list[prev_id]["next"] = curr_id
            curr_id = prev_id
   
        return linked_list
    
    def _create_next_button(self):
        """Create a next button to this window"""
        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self._next_button_on_click)
        size_hint = next_button.sizeHint()
        next_button.setFixedWidth(size_hint.width())
        self.hlayout.addWidget(next_button)

    def _create_prev_button(self):
        """Create a next button to this window"""
        prev_button = QPushButton("Previous", self)
        prev_button.clicked.connect(self._prev_button_on_click)
        size_hint = prev_button.sizeHint()
        prev_button.setFixedWidth(size_hint.width())
        self.hlayout.addWidget(prev_button)

    def _prev_button_on_click(self):
        prev_id = self.linked_list[self.current_graph_id]["prev"]
        if prev_id != -1:
            self.current_graph_id = prev_id
            self.graph_obj = self.linked_list[self.current_graph_id]["graph"]
            # self.graph = GraphCanvas(self.parent, graph=self.graph_obj, width=5, height=6, dpi=100)
            self.graph.refresh(self.graph_obj)
            n_nodes, n_edges = self.graph_obj.number_of_nodes(), self.graph_obj.number_of_edges()
            self.text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}"
            self.info_tab.setText(self.text)
      

    def _next_button_on_click(self):
        next_id = self.linked_list[self.current_graph_id]["next"]
        if next_id != -1:
            self.current_graph_id = next_id
            self.graph_obj = self.linked_list[self.current_graph_id]["graph"]
            self.graph.refresh(self.graph_obj)
           
            n_nodes, n_edges = self.graph_obj.number_of_nodes(), self.graph_obj.number_of_edges()
            self.text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}"
            self.info_tab.setText(self.text)
   

