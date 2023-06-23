from ..action import GlobalAction
from ...static import PageState


class Info(GlobalAction):

    def do(self):
        PageState.welcome_page.show()
