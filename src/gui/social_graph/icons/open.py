from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_global_action
from src.actions.global_actions import Load


class OpenIcon(IconAction):

    DESC = 'Click to open another graph.'
    FILENAME = 'open.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()

    def onclick(self):
        if self.enabled:
            perform_global_action(Load)()

    def set_enabled_or_not(self):
        self.enable()