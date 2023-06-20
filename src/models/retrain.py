from src.loaders.asnr_dataloader import ASNRGraph
from src.models.train import train_model

def retrain_model(graph, animal):
    try: 
        features, edgelist, adj, _, _ = ASNRGraph(graph_obj=graph).preprocess()
        train_model(animal, features, edgelist, adj)
     
        return True
    except Exception as error:
        print("Retraining model failed due to error: ", error)
        return False 