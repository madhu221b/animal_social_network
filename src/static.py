import os
import glob
from collections import defaultdict

import sys


def parse_readme(path):
    metadata = defaultdict(lambda: "n/a")
    with open(path, "r") as file:
        # Skip first 2 lines
        for _ in range(2):
            next(file)
        for line in file:
            data = line.split("|")
            if len(data) == 2:
                k, v = data
                metadata[k.strip()] = v.strip()
    return metadata


# ==================================================
# Constants
# ==================================================

LANDING_PAGE_TITLE = "Social Network Analysis of Animals"
LANDING_PAGE_WIDTH = 500
LANDING_PAGE_HEIGHT = 100

MAIN_WINDOW_HEIGHT = 800
MAIN_WINDOW_WIDTH = 1000

GRAPH_VERSION_FOLDER = "./results/graphs/"

with open("datasets/final_datasets.txt") as f:
    paths = [x.strip() for x in f.readlines()]

GRAPH_DATA = defaultdict(dict)

for path in paths:
    category, name, _ = path.split("/")[3:]
    metadata = parse_readme(glob.glob(os.path.join(*path.split("/")[:-1], "*.md"))[0])
    GRAPH_DATA[category][name] = {
        "path": path,
        "title": "Placeholder " + name,
        "metadata": metadata,
    }

GRAPH_DATA = dict(GRAPH_DATA)

# Generated version table
VERSIONS = {}
for category in GRAPH_DATA.keys():
    for animal in GRAPH_DATA[category].keys():
        animal_folder = os.path.join(GRAPH_VERSION_FOLDER, animal)
        VERSIONS[animal] = ["default"]
        if os.path.isdir(animal_folder):
            filenames = [x for x in os.listdir(animal_folder) if x.endswith(".pkl")]
            filenames.sort()
            VERSIONS[animal].extend([x[:-4] for x in filenames])  # removing .pkl

# ==================================================
# Variables
# ==================================================


# static class of variables
class PageState:
    id = None
    category = None
    path = None
    title = None
    # TODO move selected_nodes, selected_edges here

    @staticmethod
    def clear():
        PageState.id = None
        PageState.category = None

    @staticmethod
    def select_id(category, id):
        PageState.id = id
        PageState.category = category
        PageState.graph_path = PageState.title = GRAPH_DATA[category][id]["path"]

    @staticmethod
    def select_version(version, is_next_version=False):
        if (
            not is_next_version
        ):  # this call is called when "select" button is clicked for dropdown.
            PageState.curr_version = version
            PageState.version = version
        else:  # this call is called when "save" button is called for retraining
            # PageState.curr_version = version
            PageState.version = version
        PageState.version_path = os.path.join(
            GRAPH_VERSION_FOLDER, PageState.id, version + ".pkl"
        )
