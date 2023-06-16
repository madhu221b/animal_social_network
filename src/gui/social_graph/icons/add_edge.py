from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_action_on_graph
from src.actions.graph_actions import AddEdge


class AddEdgeIcon(IconAction):

    NAME = 'Add edge'
    FILENAME = 'add_edge.png'

    def onclick(self):
        if self.enabled:
            self.parent.graph_page.graph.deselect()
            self.parent.graph_page.graph.node_selection_changed.connect(self.try_send)

    def disconnect(self):
        try:
            self.parent.graph_page.graph.node_selection_changed.disconnect(self._try_send)
        except TypeError:
            pass

    def cancel(self):
        self.disconnect()

    def try_send(self, n_selected_nodes):
        # Wait until 2 nodes are selected
        if n_selected_nodes == 2:
            self.send()
            self.disconnect()

    def send(self):
        nodes = self.parent.graph_page.graph.selected_nodes
        edge = (nodes[0], nodes[1])
        perform_action_on_graph(self.parent.graph_page, AddEdge)(edge=edge)
        self.parent.graph_page.graph.deselect()
        self.parent.graph_page.graph.select(edges=[edge])