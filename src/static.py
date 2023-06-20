import os

# ==================================================
# Constants
# ==================================================

LANDING_PAGE_TITLE = "Social Network Analysis of Animals"
LANDING_PAGE_WIDTH = 500
LANDING_PAGE_HEIGHT = 100

MAIN_WINDOW_HEIGHT = 600
MAIN_WINDOW_WIDTH = 1000

DATA_ROOT = "./datasets"

GRAPH_DATA = {
    "bat": {
        "path": os.path.join(DATA_ROOT, "vampirebats_carter_mouth_licking_attribute_new.graphml"),
        "title": "Placeholder for bat title"
    },
    "junglefowl": {
        "path":
            os.path.join(DATA_ROOT, "junglefowl_mcdonald_sexual_network_group9_attribute.graphml"),
        "title":
            "Placeholder for junglefowl title"
    }
}

IDS = list(GRAPH_DATA.keys())

# ==================================================
# Variables
# ==================================================


# static class of variables
class PageState:
    id = None
    path = None
    title = None
    # TODO move selected_nodes, selected_edges here

    @staticmethod
    def clear():
        PageState.id = None

    @staticmethod
    def select_id(id):
        PageState.id = id
        PageState.path = GRAPH_DATA[id]["path"]
        PageState.title = GRAPH_DATA[id]["title"]