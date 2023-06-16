from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_action_on_graph
from src.actions.graph_actions import Predict


class PredEdgesIcon(IconAction):

    NAME = 'Predict edges'
    FILENAME = 'play.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable()

    def onclick(self):
        if self.enabled:
            perform_action_on_graph(self.parent.graph_page, Predict)()