from ..action import GraphAction
from ...models.retrain import retrain_model
from ...static import PageState


class Retrain(GraphAction):

    def __init__(self, *args, nodes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = self.graph_gui.graph
        self.is_retrained = self._retrain_model()
 
    def do(self):
        is_retrain_model = self.is_retrained
 

    def _retrain_model(self):
        return retrain_model(self.graph.graph, PageState.id)
  
