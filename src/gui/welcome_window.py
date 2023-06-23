import os
from PyQt6.QtWidgets import QWidget, QDialog, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QPixmap

ICON_PATH = 'res/icons/'


class TutorialPage(QWidget):

    def __init__(self, text, image_path=None, image_alignment='top', parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Create the QLabel for the image, if an image path is provided
        if image_path:
            image_label = QLabel(self)
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap)
            if image_alignment == 'top':
                layout.addWidget(image_label)

        # Add the text
        layout.addWidget(QLabel(text))

        # Add the image to the right or left of the text, if an image path is provided
        if image_path and image_alignment in ['right', 'left']:
            text_label = QLabel(text, self)
            hbox = QHBoxLayout()
            if image_alignment == 'left':
                hbox.addWidget(image_label)
                hbox.addWidget(text_label)
            else:
                hbox.addWidget(text_label)
                hbox.addWidget(image_label)
            layout.addLayout(hbox)


class WelcomeScreen(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to My Application")

        # Create the QStackedWidget
        self.pages = QStackedWidget()

        # Add the tutorial pages
        self.pages.addWidget(
            TutorialPage("This is the first page of the tutorial.",
                         image_path="path_to_image1.png"))
        self.pages.addWidget(
            TutorialPage("This is the second page of the tutorial.",
                         image_path="path_to_image2.png"))
        # Add as many pages as you need...

        # Create the navigation buttons
        self.next_button = QPushButton(QIcon(os.path.join(ICON_PATH, 'right.png')), "Next")
        self.next_button.clicked.connect(self.go_to_next_page)

        self.prev_button = QPushButton(QIcon(os.path.join(ICON_PATH, 'left.png')), "Previous")
        self.prev_button.clicked.connect(self.go_to_prev_page)

        self.skip_button = QPushButton("Skip")
        self.skip_button.clicked.connect(self.close)

        # Create the dialog layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.pages)

        # Create a QHBoxLayout for the navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.skip_button)

        layout.addLayout(button_layout)

    def go_to_next_page(self):
        if self.pages.currentIndex() < self.pages.count() - 1:
            self.pages.setCurrentIndex(self.pages.currentIndex() + 1)

    def go_to_prev_page(self):
        if self.pages.currentIndex() > 0:
            self.pages.setCurrentIndex(self.pages.currentIndex() - 1)