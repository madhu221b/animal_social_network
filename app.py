import sys
import argparse
import numpy as np
import warnings
from PyQt6.QtCore import QTimer

from src.utils.common import seed_everything
from src.static import PageState

warnings.simplefilter(action='ignore', category=FutureWarning)
np.seterr(divide='ignore', invalid='ignore')

from PyQt6 import QtWidgets, QtCore
from src.gui.landing_page import LandingPage

debug_tabs = ['social', 'analysis', 'evolution', 'faq']

parser = argparse.ArgumentParser(description='Simple settings.')
parser.add_argument('--animal', default=None)
parser.add_argument('--debug', choices=debug_tabs, default=None)

if __name__ == '__main__':

    seed_everything(42)

    # Set up default window
    app = QtWidgets.QApplication(sys.argv)
    PageState.landing_page = LandingPage()
    PageState.landing_page.show()

    # Pre-click if in debug mode
    args = parser.parse_args()

    if args.animal:
        PageState.landing_page._simulate_select(animal=args.animal)

    if args.debug:
        if not args.animal:
            PageState.landing_page._simulate_select(animal='bats')
        i = debug_tabs.index(args.debug)
        QTimer.singleShot(100, lambda: PageState.welcome_page.hide())
        QTimer.singleShot(100, lambda: PageState.landing_page.main_window.tabs.setCurrentIndex(i))
        PageState.landing_page.main_window.updateTab(i)

    sys.exit(app.exec())