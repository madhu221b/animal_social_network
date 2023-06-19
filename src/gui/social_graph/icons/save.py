from src.gui.social_graph.icons.action import IconAction

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
            # TODO
            raise NotImplementedError