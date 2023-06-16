from ..action import GraphAction
from ...models.inference import get_pred_edges
from ...static import PageState


class Predict(GraphAction):

    def __init__(self, *args, nodes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes = nodes if nodes else self._get_hanging_nodes()
        self.directed_edges = self._predict_edges()

    def do(self):
        super().do()
        self.graph_gui.add_edges(self.directed_edges)
        self.graph_gui.graph.deselect()
        self.graph_gui.graph.select(nodes=self.nodes, edges=self.directed_edges)

    def undo(self, node_data):
        super().do()
        # TODO:
        # self.graph.remove(node, coords)
        pass

    def _get_hanging_nodes(self):
        return [(n, v) for (n, v) in self.graph_gui.graph.hanging_nodes.items()]

    def _predict_edges(self):
        edges = []
        for node_name, _ in self.nodes:
            edges.extend(get_pred_edges(self.graph_gui.graph.graph, PageState.id, node_name))
        return edges
