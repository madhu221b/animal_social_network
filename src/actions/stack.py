import logging
from PyQt6.QtCore import QObject, pyqtSignal

from .action import GraphAction
from .graph_actions import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('stack')


class _ActionStack(QObject):
    done_stack = []
    undone_stack = []

    done_stack_changed = pyqtSignal(int, name="done_change")
    undone_stack_changed = pyqtSignal(int, name="undone_change")

    @staticmethod
    def add(item):
        assert isinstance(item, GraphAction), f"Action must be GraphAction, not {type(item)}"
        success = item.do()
        success = success is None or success
        if success:
            ActionStack.done_stack.append(item)
            ActionStack.undone_stack = []
            ActionStack.trigger_events()
        return success

    @staticmethod
    def undo():
        item = ActionStack.done_stack.pop()
        ActionStack.undone_stack.append(item)
        item.undo()
        ActionStack.trigger_events()

    @staticmethod
    def redo():
        if len(ActionStack.undone_stack):
            item = ActionStack.undone_stack.pop()
            ActionStack.done_stack.append(item)
            item.do()
            ActionStack.trigger_events()

    @staticmethod
    def trigger_events():
        ActionStack.done_stack_changed.emit(len(ActionStack.done_stack))
        ActionStack.undone_stack_changed.emit(len(ActionStack.undone_stack))

    @staticmethod
    def reset(trigger=True):
        ActionStack.done_stack = []
        ActionStack.undone_stack = []
        ActionStack.trigger_events()


ActionStack = _ActionStack()


def perform_action_on_graph(graph, action_class):

    def _perform_action(*args, **kwargs):
        action = action_class(graph, *args, **kwargs)
        return ActionStack.add(action)

    return _perform_action


def perform_global_action(action_class):

    def _perform_action(*args, **kwargs):
        action = action_class(*args, **kwargs)
        return action.do()
        # Note: this is a global action, not added to the stack

    return _perform_action