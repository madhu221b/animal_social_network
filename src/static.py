import os
import glob
import pickle
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
LANDING_PAGE_WIDTH = 600
LANDING_PAGE_HEIGHT = 360

MAIN_WINDOW_HEIGHT = 800
MAIN_WINDOW_WIDTH = 1040

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
    landing_page = None
    welcome_page = None
    version = None
    # TODO move selected_nodes, selected_edges here

    @staticmethod
    def clear():
        PageState.id = None
        PageState.category = None
        PageState.version = -1

    @staticmethod
    def select_id(category, id):
        PageState.id = id
        PageState.category = category
        PageState.title = f"Social Network for Category: {category}, Animal: {id}"
        PageState.graph_path = GRAPH_DATA[category][id]["path"]
        PageState.metadata = GRAPH_DATA[category][id]["metadata"]

    @staticmethod
    def select_version(version):
        PageState.version = version
        PageState.version_path = os.path.join(GRAPH_VERSION_FOLDER, PageState.id, version + ".pkl")
        if os.path.isfile(PageState.version_path):
            with open(PageState.version_path, "rb") as f:
                data = pickle.load(f)
                PageState.prev_version = data['prev_version']
                PageState.prev_path = data['prev_path']
        else:
            PageState.prev_version = None
            PageState.prev_path = None

    @staticmethod
    def step_version(new_version):
        PageState.prev_version = PageState.version
        PageState.prev_path = PageState.version_path
        PageState.version = new_version
        PageState.version_path = os.path.join(GRAPH_VERSION_FOLDER,
                                              PageState.id,
                                              new_version + ".pkl")
