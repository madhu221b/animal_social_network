from ..action import GraphAction


class AddNode(GraphAction):

    _unique_id = 0

    def __init__(self, *args, node_data, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_data = node_data
        self.node_name = f"new_node#{AddNode._unique_id}"
        self.node = (self.node_name, self.node_data)
        AddNode._unique_id += 1

    def do(self):
        super().do()
        self.graph_gui.add_node(self.node)

    def undo(self):
        super().undo()
        self.graph_gui.remove_node(self.node_name)