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
    WINDOW_HEIGHT = 100
    USER_OPTIONS = list(GRAPHS.keys())

    def __init__(self):
        super(LandingPage, self).__init__()

        # Set default layout
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.layout = QtWidgets.QHBoxLayout(
            self)  # Change to QHBoxLayout to place elements side by side

        # Add dropdown list to the window
        self._create_dropdown_list()

        # Add select button to the window
        self._create_select_button()

        # Center the window on the screen
        self._center_window()

    def _center_window(self):
        """Center the window on the screen"""
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.WINDOW_WIDTH) // 2
        y = (screen_geometry.height() - self.WINDOW_HEIGHT) // 2
        self.move(x, y)

    def _create_dropdown_list(self):
        """Create a clickable dropdown list to this window"""
        dropdown_list = DropDownListBox(self)

        # Define all choices the users can choose from
        dropdown_list.addItems(self.USER_OPTIONS)
        dropdown_list.setCurrentIndex(0)  # Select the first item by default

        # Add widget to the layout
        self.layout.addWidget(dropdown_list)
        self.dropdown_list = dropdown_list

    def _create_select_button(self):
        """Create a select button to this window"""
        select_button = QtWidgets.QPushButton("Select", self)

        # Set click event
        select_button.clicked.connect(self._select_button_on_click)

        # Calculate the preferred size of the button
        size_hint = select_button.sizeHint()

        # Set the fixed width based on the preferred size
        select_button.setFixedWidth(size_hint.width())

        # Add widget to the layout
        self.layout.addWidget(select_button)

    def _select_button_on_click(self):
        """
        When user clicks the select button, close this 'menu' window
        and open the desired dashboard
        """

        # Select item
        item = self.dropdown_list.currentText()
        print("Item Selected:", item)

        # In case we already opened, close the previous one
        if hasattr(self, "main_window"):
            # TODO what if we keep all canvas and just show and hide them
            self.main_window.destroy()

        # Create new window and hide this one
        self.main_window = MainCanvas(text=item)
        self.main_window.show()
        self.hide()

    def _simulate_select_first_item(self):
        """Simulate selecting the first item for development purposes"""
        self.dropdown_list.setCurrentIndex(0)
        self._select_button_on_click()


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    dropdown_window = LandingPage()
    dropdown_window.show()
    sys.exit(app.exec_())