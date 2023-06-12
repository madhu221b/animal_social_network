from PyQt5 import QtCore, QtWidgets
from .canvas import MainCanvas, GRAPHS


class DropDownListBox(QtWidgets.QComboBox):
    popup_dropdown_window = QtCore.pyqtSignal()

    def showPopup(self):
        self.popup_dropdown_window.emit()
        super(DropDownListBox, self).showPopup()


class LandingPage(QtWidgets.QWidget):
    """
    This is the dropdown menu that appears first on the screen.
    The user is given a list of choices from which she can choose from,
    and when one item is chosen, this window is closed and another window
    with the chosen content pops up.
    """

    WINDOW_TITLE = "Social Network Analysis of Animals"
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 300
    USER_OPTIONS = list(GRAPHS.keys())

    def __init__(self):
        super(LandingPage, self).__init__()

        # Set default layout
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.layout = QtWidgets.QVBoxLayout(self)

        # Add dropdown list to the window
        self._create_dropdown_list()

    def _create_dropdown_list(self):
        """Create a clickable dropdown list to this window"""
        dropdown_list = DropDownListBox(self)

        # Define all choices the users can choose from
        self._add_default_choices_to_dropdown(dropdown_list)

        # Set click events
        dropdown_list.view().pressed.connect(self._dropdown_on_click)

        # Add widget to the layout
        self.layout.addWidget(dropdown_list)
        self.dropdown_list = dropdown_list

    def _add_default_choices_to_dropdown(self, drop_down_list: DropDownListBox):
        """Creating a list of choices the users can choose from"""

        def _populate_combo():
            if not drop_down_list.count():
                drop_down_list.addItems(self.USER_OPTIONS)

        drop_down_list.popup_dropdown_window.connect(_populate_combo)

    def _dropdown_on_click(self, index: int):
        """When user selects an item by clicking on it, close this 'menu' window
           and open the desired dashboard
        """

        # Select item
        item = self.dropdown_list.model().itemFromIndex(index)
        print("Item Selected:", item.text())

        # In case we already opened, close the previous one
        if hasattr(self, "main_window"):
            # TODO what if we keep all canvas and just show and hide them
            self.main_window.destroy()

        # Create new window and hide this one
        self.main_window = MainCanvas(text=item.text())
        self.main_window.show()
        self.hide()


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    dropdown_window = LandingPage()
    dropdown_window.show()
    sys.exit(app.exec_())