import sys
import argparse
import numpy as np
import warnings

from src.utils.common import seed_everything

warnings.simplefilter(action='ignore', category=FutureWarning)
np.seterr(divide='ignore', invalid='ignore')

from PyQt6 import QtWidgets, QtCore
from src.gui.landing_page import LandingPage

parser = argparse.ArgumentParser(description='Simple settings.')
parser.add_argument('--debug', action='store_true')

if __name__ == '__main__':

    seed_everything(42)

    # Set up default window
    app = QtWidgets.QApplication(sys.argv)
    window = LandingPage()
    window.show()

    # Pre-click if in debug mode
    args = parser.parse_args()
    if args.debug:
        window._simulate_select_first_item()
        # Add any simulated actions here that speeds up your tests

    sys.exit(app.exec())