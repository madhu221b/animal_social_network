from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_global_action
from src.actions.global_actions import Load


class OpenIcon(IconAction):

    NAME = 'Load graph'
    FILENAME = 'open.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()

    def onclick(self):
        if self.enabled:
            perform_global_action(Load)()