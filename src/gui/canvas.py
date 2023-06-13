import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTabWidget

from src.gui.graph_analytics import GraphAnalytics
from .social_graph import GraphPage


class MainCanvas(QMainWindow):
    """
    This is the main window, with tabs and 1 canvas (dashboard/page) for each tab.
    """

    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 1000

    def __init__(self, text, *args, **kwargs):
        super(MainCanvas, self).__init__(*args, **kwargs)
        self.text = text
        self.setWindowTitle(text)
        self.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(widget)
        self.setLayout(self.layout)
        self.setCentralWidget(widget)

        # Add pages
        tabs = QTabWidget()
        self.graph_page = GraphPage(self)
        self.graph_analytics = GraphAnalytics(self)
        tabs.addTab(self.graph_page, "Social Graph")
        tabs.addTab(self.graph_analytics, "Graph Analytics")
        self.layout.addWidget(tabs)

        # Center the window on the screen
        self._center_window()

    def _center_window(self):
        """Center the window on the screen"""
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.WINDOW_WIDTH) // 2
        y = (screen_geometry.height() - self.WINDOW_HEIGHT) // 2
        self.move(x, y)

    # def _create_graph_page(self):
    #     """
    #      The Graph Visualization
    #     """
    #     tab = QWidget()
    #     layout = QHBoxLayout()

    #     self.graph_page = GraphCanvas(self, width=5, height=4, dpi=100)

    #     layout.addWidget(QLabel("Left"))
    #     layout.addWidget(self.graph_page)
    #     layout.addWidget(QLabel("Right"))
    #     tab.setLayout(layout)
    #     return tab

    # def NodeUI(self):
    #     generalTab = QWidget()
    #     layout = QVBoxLayout()
    #     self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
    #     self.toolbar = NavigationToolbar2QT(self.canvas, self)
    #     # layout.addWidget(self.toolbar)
    #     layout.addWidget(self.canvas)
    #     generalTab.setLayout(layout)
    #     return generalTab

    # def SliderUI(self):
    #     widget = QWidget()
    #     layout = QVBoxLayout()

    #     slider_b = BSlider(title="Betweenness Centrality")
    #     layout.addWidget(slider_b)

    #     slider_c = CSlider(title="Closeness Centrality")
    #     layout.addWidget(slider_c)
    #     widget.setLayout(layout)
    #     return widget
