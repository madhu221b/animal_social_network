from abc import ABC
from PyQt6.QtCore import pyqtSignal

from ..gui.social_graph.graph import GraphCanvas


class Action:
    """
    General actions that can be performed
    """

    def __init__(self):
        self.done = False

    def do(self):
        """Performing action"""
        self.done = True


class NavigationAction(Action):
    """
    These are the actions like 'save graph' or 'exit graph'
    """
    pass


class GraphAction(Action):
    """
    These are the actions that operate on the graph canvas, e.g. add/remove nodes
    """
    signal = pyqtSignal(tuple)

    def __init__(self, graph_gui: GraphCanvas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_gui = graph_gui

    def undo(self):
        """Undoing action on graph"""
        self.done = False
