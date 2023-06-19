from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import matplotlib

matplotlib.use("Qt5Agg")

from .graph import GraphCanvas
from .side_bar import NodeInfoPage
from .icons import AddNodeIcon, UndoIcon, PredEdgesIcon, AddEdgeIcon, RedoIcon


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
        layout = QHBoxLayout()

        # Sub-pages definition
        self.graph_page = GraphCanvas(parent, width=5, height=4, dpi=100)
        self.left_page = NodeInfoPage(self.graph_page.features, self.graph_page.metrics)
        self.right_page = NodeInfoPage(self.graph_page.features, self.graph_page.metrics)

        # Sub-pages allocation on main page
        layout.addWidget(self.left_page)
        layout.addWidget(self.graph_page)
        layout.addWidget(self.right_page)
        self.setLayout(layout)

    def _create_tool_bar(self):

        # Define menu/toolbar
        self.toolbar = QToolBar(self.parent)
        action = QAction("Action", self.parent)
        self.toolbar.addAction(action)
        # self.parent.addToolBar(Qt.ToolBarArea, self.toolbar)

        # Icons listed from top to bottom
        self.icons = {
            "add_node": AddNodeIcon(self),
            "add_edge": AddEdgeIcon(self),
            "undo": UndoIcon(self),
            "redo": RedoIcon(self),
            "pred": PredEdgesIcon(self)
        }
        for action in list(self.icons.values()):
            self.toolbar.addAction(action)

    def refresh(self):
        self.graph_page.refresh()
        self.icons["pred"].refresh(self.graph_page.graph.predictable)