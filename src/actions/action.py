from abc import ABC


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

    def __init__(self, graph, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.graph = graph

    def undo(self):
        """Undoing action on graph"""
        self.done = False

