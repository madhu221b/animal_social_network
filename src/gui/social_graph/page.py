from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolBar, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import matplotlib

matplotlib.use("Qt5Agg")

from .graph import GraphCanvas
from .side_bar import NodeInfoPage
from .info_page import InfoPage
from .color_bar import ColorBar
from .icons import AddNodeIcon, UndoIcon, PredEdgesIcon, AddEdgeIcon, RedoIcon, SaveIcon, OpenIcon, InfoIcon
from .matrix import FullScreenWidget
from src.static import PageState


class GraphPage(QWidget):
    """
    This is the page that belongs to the "graph" tab. It consists of three sub-pages:
     - Left page: shows information about the object which is hovered by the mouse
     - Graph page: shows the graph of animals
     - Right page: shows information about the selected object (the one last clicked on)
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Toolbar
        self._create_tool_bar()

        # Page
        main_layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        content_layout = QVBoxLayout()

        # Sub-pages definition
        self.versionlabel = QLabel("Version: " + PageState.version)
        self.graph_page = GraphCanvas(parent, width=5, height=2, dpi=100)
        self.left_page = NodeInfoPage(self.graph_page.features, self.graph_page.metrics)
        self.right_page = NodeInfoPage(self.graph_page.features, self.graph_page.metrics, title="Selected Node")
        self.top_page = InfoPage(self.graph_page.graph.graph)
        self.color_bar = ColorBar(parent, self.graph_page.graph.graph)
        self.adj_matrix = FullScreenWidget(self.graph_page.graph, self)
        self.button = QPushButton("Adjacency Matrix")

        # button functionality
        self.button.clicked.connect(self.adj_matrix.showMaximized)
        self.button.setStyleSheet("font-size: 24px; padding 10px;")

        # Add content
        content_layout.addWidget(self.versionlabel, 1)
        content_layout.addWidget(self.graph_page, 7)
        content_layout.addWidget(self.color_bar, 2)
        content_layout.addWidget(self.top_page, 1)
        content_layout.addWidget(self.button, 1)
        
        # Set margins
        content_layout.setSpacing(0)

        # Sub-pages allocation on main page
        hlayout.addWidget(self.left_page)
        hlayout.addLayout(content_layout)
        hlayout.addWidget(self.right_page)
        self.right_page.hide()

        main_layout.addLayout(hlayout)

        self.setLayout(main_layout)

    def _create_tool_bar(self):

        # Define menu/toolbar
        self.toolbar = QToolBar(self.parent)
        self.parent.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        # Icons listed from top to bottom
        self.icons = {
            "add_node": AddNodeIcon(self),
            "add_edge": AddEdgeIcon(self),
            "undo": UndoIcon(self),
            "redo": RedoIcon(self),
            "pred": PredEdgesIcon(self),
            "save": SaveIcon(self),
            "open": OpenIcon(self),
            "info": InfoIcon(self)
        }
        for action in list(self.icons.values()):
            self.toolbar.addAction(action)

    def disable_social_graph_menu(self):
        for icon in self.icons.values():
            icon.disable()
        self.icons["info"].enable()
        self.icons["open"].enable()

    def enable_social_graph_menu(self):
        for icon in self.icons.values():
            icon.set_enabled_or_not()

    def refresh(self):
        self.graph_page.refresh()
        self.top_page.refresh(self.graph_page.graph.graph)
        self.icons["pred"].refresh(self.graph_page.graph.predictable)