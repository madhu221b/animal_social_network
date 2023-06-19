import networkx as nx
import glob
import os
import matplotlib.pyplot as plt

animal_classes = [
    "Aves",
    "Amphibia",
    "Insecta",
    "Cephalapoda",
    "Actinopterygii",
    "Reptilia",
    "Arachnid",
    "Mammalia",
]


def load_graph(path):
    # print(path)
    g = nx.read_graphml(path)
    remove_arr = []
    for node, data in g.nodes(data=True):
        if len(data.keys()) < 10:
            remove_arr.append(node)
    [g.remove_node(node) for node in remove_arr]
    return g


def test(min_individuals, min_attributes):
    i = 0
    with open(f"{min_individuals}+n_{min_attributes}+f_graphs.txt", "w") as f:
        casi = set()
        for animal_class in animal_classes:
            files = glob.glob(os.path.join(data_path, animal_class, "*/**.graphml"))
            for file in files:
                g = nx.read_graphml(file)
                remove_arr = []
                for node, data in g.nodes(data=True):
                    if len(data.keys()) < min_attributes:
                        remove_arr.append(node)
                [g.remove_node(node) for node in remove_arr]
                if g.number_of_nodes() > min_individuals:
                    f.write(file + "\n")
                    casi.add(file.split("/")[4])
                    i += 1
        f.write(f"{i} number of lines, {len(casi)} situations")
    return i, len(casi)


MIN_ATTRIBUTES = [x for x in range(1, 11, 3)]
# MIN_INDIVIDUALS = [x for x in range(5, 20, 5)]
#
MIN_INDIVIDUALS = [0]


if __name__ == "__main__":
    data_path = "./asnr/Networks/"

    for a in MIN_INDIVIDUALS:
        for b in MIN_ATTRIBUTES:
            print(
                f" Config min N/F {a}/{b} gets (# of lines, # of uniques)", test(a, b)
            )
    print("Complete!")
    # print(files[0])
