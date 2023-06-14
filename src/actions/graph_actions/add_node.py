
from ..action import GraphAction

class AddNode(GraphAction):

    def do(self, node):
        super().do()
        # TODO:
        # self.node = node
        # self.coords = ...
        # self.graph.add(self.node, self.coords)
        pass

    def undo(self, node):
        super().do()
        # TODO:
        # self.graph.remove(node, coords)
        pass