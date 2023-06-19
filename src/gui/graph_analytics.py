from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel

class GraphAnalytics(QWidget):
    """
     Add the necessary comments
    """

    def __init__(self, parent):
        super().__init__()
        self.layout = QHBoxLayout()     
        self.layout.addWidget(QLabel("TODO here for Graph Analytics"))
        self.setLayout(self.layout)
        