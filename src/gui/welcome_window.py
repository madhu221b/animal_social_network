import os
import json
from PyQt6.QtWidgets import QWidget, QDialog, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore

from .custom_buttons import SmallGreenButton

ICON_PATH = 'res/icons/'
JSON_PATH = 'res/welcome.json'


class TutorialPage(QWidget):

    def __init__(self, text, image_path=None, image_alignment='top', parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Create the QLabel for the image, if an image path is provided
        if image_path:
            image_label = QLabel(self)
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            if image_alignment == 'top':
                # Create a QHBoxLayout, add stretches on either side of the image
                hbox = QHBoxLayout()
                hbox.addStretch()
                hbox.addWidget(image_label)
                hbox.addStretch()
                layout.addLayout(hbox)

        # Add the text
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

        # Add the image to the right or left of the text, if an image path is provided
        if image_path and image_alignment in ['right', 'left']:
            hbox = QHBoxLayout()
            hbox.setSpacing(20)
            if image_alignment == 'left':
                hbox.addWidget(image_label)
                hbox.addWidget(text_label)
            else:
                hbox.addWidget(text_label)
                hbox.addWidget(image_label)
            hbox.addStretch()
            layout.addLayout(hbox)


class WelcomeScreen(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to My Application")
        self.setFixedSize(400, 300)

        # Create pages
        self.pages = QStackedWidget()
        with open(JSON_PATH, "r") as f:
            contents = json.loads(f.read())
        for content in contents:
            self.pages.addWidget(TutorialPage(**content))

        # Create the navigation buttons
        self.next_button = QPushButton(QIcon(os.path.join(ICON_PATH, 'right.png')), "Next")
        self.next_button.clicked.connect(self.go_to_next_page)

        self.prev_button = QPushButton(QIcon(os.path.join(ICON_PATH, 'left.png')), "Previous")
        self.prev_button.clicked.connect(self.go_to_prev_page)

        self.close_button = SmallGreenButton("Close")
        self.close_button.clicked.connect(self.hide)

        # Create the dialog layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.pages)

        # Create a QHBoxLayout for the navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        self.update_buttons()

    def go_to_next_page(self):
        if self.pages.currentIndex() < self.pages.count() - 1:
            self.pages.setCurrentIndex(self.pages.currentIndex() + 1)
        self.update_buttons()

    def go_to_prev_page(self):
        if self.pages.currentIndex() > 0:
            self.pages.setCurrentIndex(self.pages.currentIndex() - 1)
        self.update_buttons()

    def update_buttons(self):
        # Disable the previous button on the first page
        self.prev_button.setEnabled(self.pages.currentIndex() != 0)
        # Disable the next button on the last page
        self.next_button.setEnabled(self.pages.currentIndex() != self.pages.count() - 1)
