import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtGui import QGuiApplication

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
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - MAIN_WINDOW_WIDTH) // 2
        y = (screen_geometry.height() - MAIN_WINDOW_HEIGHT) // 2
        self.move(x, y)
