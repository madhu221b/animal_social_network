import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolBar, QAction, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib

matplotlib.use("Qt5Agg")

from .graph import GraphCanvas
from .side_bar import NodeInfoPage


class GraphPage(QWidget):
    """
    This is the page that belongs to the "graph" tab. It consists of three sub-pages:
     - Left page: shows information about the object which is hovered by the mouse
     - Graph page: shows the graph of animals
     - Right page: shows information about the selected object (the one last clicked on)
    """

    def __init__(self, parent):
        super().__init__()

        self.actions = {
            "add": "add.png", "undo": "undo.png", "open": "open.png", "save": "save.png"
        }

        self.parent = parent
        self._create_tool_bars()

        layout = QHBoxLayout()
        self.graph_page = GraphCanvas(parent, width=5, height=4, dpi=100)
        self.left_page = NodeInfoPage(self.graph_page.features, self.graph_page.metrics)
        self.right_page = NodeInfoPage(self.graph_page.features, self.graph_page.metrics)
        layout.addWidget(self.left_page)
        layout.addWidget(self.graph_page)
        layout.addWidget(self.right_page)
        self.setLayout(layout)

    def _create_tool_bars(self):
        self.toolbar = QToolBar(self.parent)
        self.parent.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        self.icon_actions = {}
        for action, img_filename in self.actions.items():
            self.icon_actions[action] = QAction(self)
            icon = QIcon(f"./res/icons/{img_filename}")
            self.icon_actions[action].setIcon(icon)
            self.icon_actions[action].setToolTip(
                action)  # Set tooltip to display action name on hover
            self.toolbar.addAction(self.icon_actions[action])

        # Connect the 'add' action to the _add_action method
        self.icon_actions['add'].triggered.connect(self._add_action)

    def _add_action(self):
        # Show a pop-up window when 'add' icon is clicked
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Add action was clicked!")
        msgBox.setWindowTitle("Add Action")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def _undo_action(self):
        pass

    def _delete_action(self):
        pass

    def _open_action(self):
        pass

    def _save_action(self):
        pass