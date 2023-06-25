from ..action import GraphAction
from ...models.inference import get_pred_edges
from ...static import PageState


class Predict(GraphAction):

    def __init__(self, *args, nodes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._nodes = nodes

    def do(self):
        super().do()
        self.nodes = self._nodes if self._nodes else self._get_hanging_new_nodes()
        self.directed_edges, self.success = self._predict_edges()
        if self.success:
            self._edges_were = self.graph_gui.graph.selected_directed_edges
            self._nodes_were = self.graph_gui.graph.selected_nodes
            self.graph_gui.add_edges(self.directed_edges)
            self.graph_gui.graph.deselect()
            self.graph_gui.graph.select(nodes=self.nodes, edges=self.directed_edges)
        return self.success

    def undo(self):
        super().undo()
        self.graph_gui.remove_edges(self.directed_edges)
        self.graph_gui.graph.deselect()
        self.graph_gui.graph.select(nodes=self._nodes_were, edges=self._edges_were)

    def _get_hanging_new_nodes(self):
        return self.graph_gui.graph.unpredicted_new_node_names

    def _predict_edges(self):
        edges = []
        for node_name in self.nodes:
            try:
                edges.extend(get_pred_edges(self.graph_gui.graph.graph, PageState.id, node_name))
            except:
                return None, False
        return edges, True
