import os
import pickle
from src.loaders.asnr_dataloader import ASNRGraph
from src.models.train import train_model


def load_pickle(file_name):
    file = open(file_name, 'rb')
    data = pickle.load(file)
    file.close()
    return data


def dump_pkl(content, file_name):
    file = open(file_name, 'wb')
    pickle.dump(content, file)
    file.close()


def retrain_model(graph, animal):
    try: 
        features, edgelist, adj, _, _ = ASNRGraph(graph_obj=graph).preprocess()
        # Retrain model
        train_model(animal, features, edgelist, adj)
        
        # Save this graph as base graph for future iterations
        save_graph(graph, animal)
        return True
    except Exception as error:
        print("Retraining model failed due to error: ", error)
        return False 


def save_graph(graph, animal):
    graph_folder = f"results/graphs/{animal}"
    if not os.path.exists(graph_folder):
         os.makedirs(graph_folder)
         id = 0
    else:
        file_names = [_ for _ in os.listdir(graph_folder)]
        if not file_names:
            max_id = -1 
        else:
            ids = [int(_.split("_")[-1]) for _ in file_names]
            max_id = max(ids)
        id = max_id + 1


    file_name = f"graph_{animal}_{id}"
    file_path = os.path.join(graph_folder, file_name)
    print(file_path)
    dump_pkl(graph, file_path)