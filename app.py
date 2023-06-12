import sys

from PyQt5 import QtWidgets
from src.dashboard.landing_page import LandingPage

app = QtWidgets.QApplication(sys.argv)
window = LandingPage()
window.show()
sys.exit(app.exec_())