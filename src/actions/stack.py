from .action import GraphAction
from .graph_actions import *


class ActionStack:
    _done_stack = []
    _undone_stack = []

    @staticmethod
    def add(item):
        assert isinstance(item, GraphAction), f"Action must be GraphAction, not {type(item)}"
        item.do()
        ActionStack._done_stack.append(item)
        ActionStack._undone_stack = []

    @staticmethod
    def undo():
        item = ActionStack._done_stack.pop()
        ActionStack._undone_stack.append(item)
        item.undo()

    @staticmethod
    def redo():
        if len(ActionStack._undone_stack):
            item = ActionStack._undone_stack.pop()
            ActionStack._done_stack.append(item)
            item.do()


def perform_action_on_graph(graph, action_class):

    def _perform_action(**kwargs):
        action = action_class(graph, **kwargs)
        ActionStack.add(action)

    return _perform_action