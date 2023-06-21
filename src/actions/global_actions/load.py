import logging
import os
import pickle

from ..action import GlobalAction
from ...static import PageState
from ...graph import Graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('load.action')


class Load(GlobalAction):

    def __init__(self, graph_gui, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_gui = graph_gui
        self.filepath = filepath

    def do(self):
        self.graph_gui.graph = Load.get_graph(self.filepath)
        self.graph_gui.refresh()
        logger.info(f"Graph loaded from {self.filepath}")

    @staticmethod
    def get_graph(filepath: str) -> Graph:
        is_default = filepath.endswith('.graphml')
        if is_default:
            return Graph.from_file(filepath)
        else:
            return Graph.from_pkl(filepath)