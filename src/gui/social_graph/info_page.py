from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class InfoPage(QWidget):

    def __init__(self, graph):
        super(InfoPage, self).__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
        self.text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}, Type of interaction: "
        self.info_tab = QLabel(parent=self, text=self.text, 
            alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_tab)
    
        self.layout.addStretch(1)
    
    def refresh(self,graph):
        n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
        text = f"Number of nodes: {n_nodes}, Number of edges: {n_edges}, Type of interaction: "
        self.info_tab.setText(text)


