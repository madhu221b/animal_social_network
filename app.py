import sys
import argparse
import numpy as np
import warnings

from src.utils.common import seed_everything
from src.static import PageState

warnings.simplefilter(action='ignore', category=FutureWarning)
np.seterr(divide='ignore', invalid='ignore')

from PyQt6 import QtWidgets, QtCore
from src.gui.landing_page import LandingPage

parser = argparse.ArgumentParser(description='Simple settings.')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--page', type=str, nargs='+', default=[])

if __name__ == '__main__':

    seed_everything(42)

    # Set up default window
    app = QtWidgets.QApplication(sys.argv)
    PageState.landing_page = LandingPage()
    PageState.landing_page.show()

    # Pre-click if in debug mode
    args = parser.parse_args()
    if len(args.page):
        PageState.landing_page._simulate_select_first_item(" ".join(args.page))

    sys.exit(app.exec())