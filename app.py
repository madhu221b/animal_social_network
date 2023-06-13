import sys
import argparse

from PyQt5 import QtWidgets, QtCore
from src.gui.landing_page import LandingPage

parser = argparse.ArgumentParser(description='Simple settings.')
parser.add_argument('--debug', action='store_true')

if __name__ == '__main__':

    # Set up default window
    app = QtWidgets.QApplication(sys.argv)
    window = LandingPage()
    window.show()

    # Pre-click if in debug mode
    args = parser.parse_args()
    if args.debug:
        window._simulate_select_first_item()
        # Add any simulated actions here that speeds up your tests

    sys.exit(app.exec_())