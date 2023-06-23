from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_global_action
from src.actions.global_actions import Info


class InfoIcon(IconAction):

    DESC = 'Click to re-open the tutorial.'
    FILENAME = 'info.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()

    def onclick(self):
        if self.enabled:
            perform_global_action(Info)()