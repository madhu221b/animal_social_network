
from .action import GraphAction

class GraphActionStack:

    def __init__(self):
        self.done_stack = []
        self.undone_stack = []

    def add(self, item):
        assert isinstance(item, GraphAction), f"Action must be GraphAction, not {type(item)}"
        self.done_stack.append(item)
        self.undone_stack = []

    def undo(self):
        item = self.done_stack.pop()
        self.undone_stack.append(item)
        item.undo()

    def redo(self):
        if len(self.undone_stack):
            item = self.undone_stack.pop()
            self.done_stack.append(item)
            item.do()