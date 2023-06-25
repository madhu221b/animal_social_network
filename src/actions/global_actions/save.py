import logging
import os
import pickle

from ..action import GlobalAction
from ...static import PageState, GRAPH_VERSION_FOLDER, VERSIONS
from ...graph import Graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("save.action")


class Save(GlobalAction):
    def __init__(self, graph, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = graph

    def do(self):
        filepath = PageState.version_path
        curr_version = PageState.curr_version
        os.makedirs(os.path.split(filepath)[0], exist_ok=True)
        graph_dict = {"prev_version": curr_version, "graph": self.graph.state_dict}
        with open(filepath, "wb") as f:
            pickle.dump(self.graph.state_dict, f)
        logger.info(f"Graph saved to {filepath}")
