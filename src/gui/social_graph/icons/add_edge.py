import logging

from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_action_on_graph
from src.actions.graph_actions import AddEdge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AddEdgeIcon')


class AddEdgeIcon(IconAction):

    DESC = 'Click to add a new edge. Select two nodes before or after this event.'
    FILENAME = 'add_edge.png'

    def onclick(self):
        if self.enabled:
            logger.info("Registered click.")
            self.parent.graph_page.graph.node_selection_changed.connect(self.try_send)
            self.try_send(self.parent.graph_page.graph.selected_nodes)

    def disconnect(self):
        logger.info("Disconnecting")
        try:
            self.parent.graph_page.graph.node_selection_changed.disconnect(self.try_send)
        except TypeError:
            logger.info("Ran into TypeError")
            pass

    def cancel(self):
        logger.info("Cancelling")
        self.parent.graph_page.graph.deselect()
        self.disconnect()

    def try_send(self, selected_nodes):
        # Wait until 2 nodes are selected
        logger.info(f"Trying to send {selected_nodes}")
        if len(selected_nodes) == 2:
            self.send()
            self.disconnect()

    def send(self):
        nodes = self.parent.graph_page.graph.selected_nodes
        logger.info(f"Sending {nodes}")
        edge = (nodes[0], nodes[1])
        perform_action_on_graph(self.parent.graph_page, AddEdge)(edge=edge)
        self.parent.graph_page.graph.deselect()
        self.parent.graph_page.graph.select(edges=[edge])