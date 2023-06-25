import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget
from PyQt6.QtGui import QGuiApplication

from src.gui.graph_analytics import GraphAnalytics
from .social_graph import GraphPage
from .faq import FAQPage
from .welcome_window import WelcomeScreen
from .evolution import GraphEvolution
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
        self.faq_page = FAQPage(self)
        PageState.welcome_page = WelcomeScreen(self)
        self.graph_analytics = None
        self.graph_evolution = None

        self.tabs.addTab(self.graph_page, "Social Graph")
        self.tabs.addTab(QWidget(), "Graph Analytics")
        

        # if GraphEvolution.should_be_visible():
        self.tabs.addTab(QWidget(), "Evolution of the Network")
        
        self.tabs.addTab(QWidget(), "FAQ")
        self.tabs.tabBarClicked.connect(self.updateTab)
        self.layout.addWidget(self.tabs)

        # Center the window on the screen
        self._center_window()

        PageState.welcome_page.show()

    def updateTab(self, tabIndex):
        if tabIndex == 1:
            self.updateGraphTab()
        elif tabIndex == 2 and GraphEvolution.should_be_visible():
            self.updateGraphEvolveTab()
        elif tabIndex == 3:
            self.openFAQTab()

    def updateGraphTab(self):
        self.tabs.removeTab(1)
        self.graph_analytics = GraphAnalytics(self)
        self.tabs.insertTab(1, self.graph_analytics, "Graph Analytics")  # <--- add tab

    def updateGraphEvolveTab(self):
        self.tabs.removeTab(2)
        self.graph_evolution = GraphEvolution(self)
        self.tabs.insertTab(2, self.graph_evolution, "Evolution of the Network")
    
    def openFAQTab(self):
        self.tabs.removeTab(3)
        self.faq_page = FAQPage(self)
        self.tabs.insertTab(3, self.faq_page, "FAQ")

    def _center_window(self):
        """Center the window on the screen"""
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - MAIN_WINDOW_WIDTH) // 2
        y = (screen_geometry.height() - MAIN_WINDOW_HEIGHT) // 2
        self.move(x, y)
