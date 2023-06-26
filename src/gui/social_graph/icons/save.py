from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_global_action
from src.actions.global_actions import Retrain, Save
from src.actions.stack import ActionStack
from src.gui.action_forms.notification import notify_user


class SaveIcon(IconAction):
    DESC = 'Click to save the current graph to disk.'
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
            success = perform_global_action(Retrain)(graph_gui=self.parent.graph_page)
            if success:
                perform_global_action(Save)(graph=self.parent.graph_page.graph)
                notify_user("Training was successful!", success=True)
            else:
                notify_user(
                "Training was unsuccessful! <br />" + \
                "It's likely you don't have many nodes to train with.",
                success=False)