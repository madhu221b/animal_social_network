from ..action import GraphAction


class AddNode(GraphAction):

    _unique_id = 0

    def __init__(self, *args, node_data, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_data = node_data
        new_node_names =[ node_name for node_name in self.graph_gui.graph.graph.nodes() if node_name.startswith("new_node")]
        if new_node_names:
            AddNode._unique_id = max([int(_.split("#")[-1]) for _ in new_node_names])+1
        self.node_name = f"new_node#{AddNode._unique_id}"
        self.node = (self.node_name, self.node_data)
        AddNode._unique_id += 1

    def do(self):
        super().do()
        self.graph_gui.add_node(self.node)

    def undo(self):
        super().undo()
        self.graph_gui.remove_node(self.node_name)