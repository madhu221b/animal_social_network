from src.gui.social_graph.icons.action import IconAction
from src.actions.stack import perform_action_on_graph
from src.actions.graph_actions import Predict
from src.gui.action_forms.notification import notify_user


class PredEdgesIcon(IconAction):

    DESC = 'Click to predict new nodes that have no edges yet.'
    FILENAME = 'play.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable()

    def onclick(self):
        if self.enabled:
            success = perform_action_on_graph(self.parent.graph_page, Predict)()
            if success:
                notify_user("Prediction was successful!", success=True)
            else:
                notify_user(
                "Prediction was unsuccessful! <br />" + \
                "It's likely you don't have a trained model yet.",
                success=False)

    def set_enabled_or_not(self):
        if self.parent.graph_page.graph.predictable:
            self.enable()
        else:
            self.disable()