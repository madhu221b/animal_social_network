from ..action import GraphAction


class AddNode(GraphAction):

    _unique_id = 0

    def __init__(self, *args, node, **kwargs):
        super().__init__(*args, **kwargs)
        self.node = node
        self.id = f"new_node#{AddNode._unique_id}"
        AddNode._unique_id += 1

    def do(self):
        super().do()
        node = (self.id, self.node)
        self.graph_gui.add_node(node)

    def undo(self, node_data):
        super().do()
        # TODO:
        # self.graph.remove(node, coords)
        pass