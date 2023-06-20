from ..action import GraphAction


class AddEdge(GraphAction):

    def __init__(self, *args, edge, **kwargs):
        super().__init__(*args, **kwargs)
        self.directed_edge = edge

    def do(self):
        super().do()
        self.graph_gui.add_edge(self.directed_edge)

    def undo(self):
        super().undo()
        self.graph_gui.remove_edge(self.directed_edge)