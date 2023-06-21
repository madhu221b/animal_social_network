import logging
import os
import pickle

from ..action import GlobalAction
from ...static import PageState
from ...graph import Graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('load.action')


class Load(GlobalAction):

    def do(self):
        PageState.landing_page.show()
