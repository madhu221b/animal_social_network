from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt
import os

from .main_window import MainWindow
from .custom_buttons import MediumGreenButton
from ..static import (
    GRAPH_DATA,
    LANDING_PAGE_TITLE,
    LANDING_PAGE_WIDTH,
    LANDING_PAGE_HEIGHT,
    PageState,
    VERSIONS,
)

INTRO_FOLDER = 'res/animal_intro'


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

    def __init__(self):
        super(LandingPage, self).__init__()

        # Set default layout
        self.setWindowTitle(LANDING_PAGE_TITLE)
        self.setGeometry(0, 0, LANDING_PAGE_WIDTH, LANDING_PAGE_HEIGHT)
        self.layout = QtWidgets.QVBoxLayout(self)

        # First, read shortcuts for animal files
        self._animal_encoder, self._animal_decoder = self._read_animal_shortcuts()

        # Add instruction
        instruction = self._create_instruction()
        self.layout.addWidget(instruction)

        # Add dropdown list
        self.button_layout = self._create_dropdown_list()
        self.layout.addLayout(self.button_layout)

        # Add horizontal line
        self.layout.addWidget(self._create_horizontal_line())

        # Fill up the rest of the window with empty space
        self.layout.addStretch()

        # Add intro page
        self.intro_layout = self._create_intro_page()
        self.layout.addLayout(self.intro_layout)

        # Add space and horizontal line again
        self.layout.addStretch()
        self.layout.addWidget(self._create_horizontal_line())

        # Add select button
        self.select_button_layout = self._create_select_button_layout()
        self.layout.addLayout(self.select_button_layout)

        # Set up trigger events
        self._create_event_connections()

        # Set initial state
        self.preset()

        # Center the window on the screen
        self._center_window()

    def show(self):
        """Bring window to the front and keep it there"""
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        super().show()

    def _read_animal_shortcuts(self):
        full_animals = list(VERSIONS.keys())
        encoder = {x: x.split('_')[0] for x in full_animals}
        decoder = {v: k for k, v in encoder.items()}
        return encoder, decoder

    def _create_horizontal_line(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return line

    def _create_instruction(self):
        label = QtWidgets.QLabel("Select Animal to analyze its Social Network")
        label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        label.setContentsMargins(0, 0, 0, 5)
        return label

    def _create_intro_page(self):
        self.intro_layout = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel(self)
        self.description_label = QtWidgets.QLabel(self)
        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                             QSizePolicy.Policy.Expanding)
        self.intro_layout.addWidget(self.image_label)
        self.intro_layout.addWidget(self.description_label)
        return self.intro_layout

    def _create_dropdown_list(self):

        FONT_FAMILY = "Arial"
        FONT_SIZE = 9
        LABEL_HEIGHT = 20
        FONT_WEIGHT = QFont.Weight.Bold

        # Define all choices the users can choose from
        self.dropdown_category = DropDownListBox(self)
        self.dropdown_list = DropDownListBox(self)
        self.dropdown_list_version = DropDownListBox(self)
        self.dropdown_category.addItems(sorted(GRAPH_DATA.keys()))
        self.dropdown_category.setCurrentIndex(0)  # Select the first item by default

        # Layouts
        taxonomy_layout = QtWidgets.QVBoxLayout()
        animal_layout = QtWidgets.QVBoxLayout()
        version_layout = QtWidgets.QVBoxLayout()
        select_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        # Taxonomy dropdown list
        taxonomy_label = QtWidgets.QLabel("Taxonomy")
        taxonomy_label.setFixedHeight(LABEL_HEIGHT)
        taxonomy_label.setFont(QFont(FONT_FAMILY, FONT_SIZE, FONT_WEIGHT))
        taxonomy_layout.addWidget(taxonomy_label)
        taxonomy_layout.addWidget(self.dropdown_category)
        taxonomy_layout.setSpacing(0)

        # Animal dropdown list
        animal_label = QtWidgets.QLabel("Animal")
        animal_label.setFixedHeight(LABEL_HEIGHT)
        animal_label.setFont(QFont(FONT_FAMILY, FONT_SIZE, FONT_WEIGHT))
        animal_layout.addWidget(animal_label)
        animal_layout.addWidget(self.dropdown_list)
        animal_layout.setSpacing(0)

        # Version dropdown list
        version_label = QtWidgets.QLabel("Version")
        version_label.setFixedHeight(LABEL_HEIGHT)
        version_label.setFont(QFont(FONT_FAMILY, FONT_SIZE, FONT_WEIGHT))
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.dropdown_list_version)
        version_layout.setSpacing(0)

        # Add buttons to the layout
        button_layout.addLayout(taxonomy_layout)
        button_layout.addLayout(animal_layout)
        button_layout.addLayout(version_layout)

        return button_layout

    @property
    def selected_animal(self):
        index = self.dropdown_list.currentIndex()
        item = self.dropdown_list.itemText(index)
        if item in self._animal_decoder:
            return self._animal_decoder[item]
        else:
            return None

    def _center_window(self):
        """Center the window on the screen"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def _create_event_connections(self):
        """Create event connections for the dropdown list and the select button"""
        self.dropdown_category.currentIndexChanged.connect(self.update_listing)
        self.dropdown_list.currentIndexChanged.connect(self.update_version_dropdown)
        self.dropdown_list.currentIndexChanged.connect(self.update_image_and_description)
        self.select_button.clicked.connect(self._select_button_on_click)

    def preset(self):
        self.update_listing(0)
        self.update_version_dropdown(0)
        self.update_image_and_description()

    def update_listing(self, index):
        """Update the version dropdown based on the selected item in the first dropdown"""
        selected_category = self.dropdown_category.itemText(index)
        self.dropdown_list.clear()
        animals = sorted(GRAPH_DATA[selected_category].keys())
        encoded_animals = [self._animal_encoder[x] for x in animals]
        self.dropdown_list.addItems(encoded_animals)

    def update_version_dropdown(self, index=None):
        """Update the version dropdown based on the selected item in the second dropdown"""
        if len(self.dropdown_list) == 0:
            return

        if index is None:
            index = self.dropdown_list.currentIndex()
        selected_animal = self._animal_decoder[self.dropdown_list.itemText(index)]
        self.dropdown_list_version.clear()
        self.dropdown_list_version.addItems(VERSIONS[selected_animal])

        if not len(VERSIONS[selected_animal]) == 1:
            self.dropdown_list_version.setEnabled(True)
        else:
            self.dropdown_list_version.setDisabled(True)

    def update_image_and_description(self):
        """Update the image and the description based on the selected item in the dropdown list"""
        # Load image
        filepath = f"{INTRO_FOLDER}/images/{self.selected_animal}.jpg"
        if os.path.isfile(filepath):
            pixmap = QPixmap(filepath)
            self.image_label.setPixmap(pixmap)

        # Load description
        filepath = f"{INTRO_FOLDER}/descriptions/{self.selected_animal}.txt"
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                description = file.read()
            self.description_label.setText(description)
        self._center_window()

    def _create_select_button_layout(self):
        """Make select button appear on right side"""
        self.select_button = self._create_select_button()
        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.select_button)
        return layout

    def _create_select_button(self):
        """Create a select button to this window"""
        select_button = MediumGreenButton("Select")

        # Calculate the preferred size of the button + set it
        size_hint = select_button.sizeHint()
        select_button.setFixedWidth(size_hint.width())
        return select_button

    def _select_button_on_click(self):
        """
        When user clicks the select button, close this 'menu' window
        and open the desired dashboard
        """

        # Select item and version
        category = self.dropdown_category.currentText()
        page_id = self._animal_decoder[self.dropdown_list.currentText()]
        page_version = self.dropdown_list_version.currentText()

        # In case we already opened, close the previous one
        if hasattr(self, "main_window"):
            # TODO what if we keep all canvas and just show and hide them
            PageState.clear()
            self.main_window.close()

        # Create new window and hide this one
        PageState.select_id(category, page_id)
        PageState.select_version(page_version)
        self.main_window = MainWindow()
        self.main_window.show()
        self.hide()

    def _simulate_select(self, animal="bats"):
        """Simulate selecting a specific item for development purposes"""
        taxonomy = {
            "barnswallow": "Aves",
            "songbird": "Aves",
            "sparrow": "Aves",
            "ants": "Insecta",
            "beetle": "Insecta",
            "baboon": "Mammalia",
            "bats": "Mammalia",
            "bison": "Mammalia",
            "groundsquirrel": "Mammalia",
            "mouse": "Mammalia",
            "rhesusmacaque": "Mammalia"
        }[animal]

        index = self.dropdown_category.findText(taxonomy)
        self.dropdown_category.setCurrentIndex(index)

        index = self.dropdown_list.findText(animal)
        self.dropdown_list.setCurrentIndex(index)

        last_index = self.dropdown_list_version.count() - 1
        self.dropdown_list_version.setCurrentIndex(last_index)

        self._select_button_on_click()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dropdown_window = LandingPage()
    dropdown_window.show()
    sys.exit(app.exec_())
