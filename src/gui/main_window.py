import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import pyqtSignal

from src.gui.graph_analytics import GraphAnalytics
from .social_graph import GraphPage
from ..static import MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH, PageState


class MainWindow(QMainWindow):
    """
    This is the main window, with tabs and 1 canvas (dashboard/page) for each tab.
    """


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(PageState.title)
        self.setGeometry(0, 0, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(widget)
        self.setCentralWidget(widget)

        # Add pages
        self.tabs = QTabWidget()
        self.graph_page = GraphPage(self)
   
        self.tabs.addTab(self.graph_page, "Social Graph")
        self.tabs.addTab(QWidget(), "Graph Analytics")
      
        self.tabs.tabBarClicked.connect(self.updateTab)
        self.layout.addWidget(self.tabs)

        # Center the window on the screen
        self._center_window()
    
    def updateTab(self, tabIndex):
        pass
        if tabIndex == 1:
            self.updateGraphTab()
    
    def updateGraphTab(self):
        self.tabs.removeTab(1)
        self.graph_analytics = GraphAnalytics(self)
        self.tabs.addTab(self.graph_analytics, "Graph Analytics") # <--- add tab


    def _center_window(self):
        """Center the window on the screen"""
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - MAIN_WINDOW_WIDTH) // 2
        y = (screen_geometry.height() - MAIN_WINDOW_HEIGHT) // 2
        self.move(x, y)
