from src.gui.social_graph.icons.action import IconAction
from src.gui.action_forms.add_node import AddNodeForm
from src.actions.stack import perform_action_on_graph
from src.actions.graph_actions import AddNode


class AddNodeIcon(IconAction):

    DESC = 'Click to add a new node.'
    FILENAME = 'add_node.png'

    def onclick(self):
        if self.enabled:
            callback = perform_action_on_graph(self.parent.graph_page, AddNode)
            self.parent.node_form = AddNodeForm(self.parent.graph_page.features, callback=callback)
            self.parent.node_form.show()

    def cancel(self):
        if hasattr(self.parent, "node_form"):
            self.parent.node_form.close()
            del self.parent.node_form

    def set_enabled_or_not(self):
        self.enable()