from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_action_on_graph
from src.actions.graph_actions import Retrain
from src.actions.stack import ActionStack



class SaveIcon(IconAction):
    NAME = 'Save'
    FILENAME = 'save.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_enabled_or_not()
        ActionStack.undone_stack_changed.connect(self.set_enabled_or_not)

    def set_enabled_or_not(self):
        if len(ActionStack.done_stack) and not self.enabled:
            self.enable()
        elif not len(ActionStack.done_stack) and self.enabled:
            self.disable()

    def onclick(self):
        if self.enabled:
            perform_action_on_graph(self.parent.graph_page, Retrain)()