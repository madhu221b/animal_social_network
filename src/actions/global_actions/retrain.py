import logging
import os
import logging
import pickle
from src.loaders.asnr_dataloader import ASNRGraph
from src.models.train import train_model

from ..action import GlobalAction
from ...static import PageState, GRAPH_VERSION_FOLDER, VERSIONS
from ..stack import ActionStack
from ...gui.action_forms.notification import notify_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("retrain.action")


class Retrain(GlobalAction):

    def __init__(self, graph_gui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_gui = graph_gui

    def do(self):

        # Determine next version id
        graph_folder = os.path.join(GRAPH_VERSION_FOLDER, str(PageState.id))
        os.makedirs(graph_folder, exist_ok=True)
        next_version = f"v{len(os.listdir(graph_folder))}"

        # Retraining graph
        features, edgelist, adj, _, _ = ASNRGraph(graph_obj=self.graph_gui.graph.graph).preprocess()
        try:
            train_model(PageState.id, next_version, features, edgelist, adj)
        except:
            return False

        logger.info("Graph retrained")

        # Increasing current version number
        VERSIONS[PageState.id].append(next_version)
        PageState.step_version(next_version)
        PageState.landing_page.update_version_dropdown()

        # Refresh on page
        self.graph_gui.graph.reset()
        ActionStack.reset()
        logger.info("Graph set as default, starting position.")
        self.graph_gui.refresh()

        return True
