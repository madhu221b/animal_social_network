from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap


class NotificationDialog(QDialog):

    def __init__(self, message:str, success:bool, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Notification")

        # Create the layout
        layout = QVBoxLayout(self)
        hbox = QHBoxLayout()

        # Create the QLabel for the icon
        icon_label = QLabel(self)
        filename = "tick" if success else "cross"
        pixmap = QPixmap(f"res/icons/{filename}.png")
        icon_label.setPixmap(pixmap)
        hbox.addWidget(icon_label)

        # Add some spacing between the icon and the message
        hbox.addSpacing(20)

        # Create the QLabel for the message
        message_label = QLabel(message)
        hbox.addWidget(message_label)

        # Add the QHBoxLayout to the main layout
        layout.addLayout(hbox)

        # Create the "Ok" button
        ok_button = QPushButton("Ok", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)


def notify_user(message:str, success:bool):
    dialog = NotificationDialog(message, success)
    dialog.exec()