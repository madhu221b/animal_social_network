import os
from PyQt6.QtGui import QAction, QIcon, QPixmap, QImage, qGray


class IconAction(QAction):

    ROOT = "./res/icons"
    NAME = None
    FILENAME = None

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.img = QPixmap(os.path.join(self.ROOT, self.FILENAME))
        self.gray_img = QPixmap(os.path.join(self.ROOT, self.FILENAME).replace(".png", "_gray.png"))
        self.icon = QIcon()
        self.icon.addPixmap(self.img, mode=QIcon.Mode.Normal, state=QIcon.State.On)
        self.disabled_icon = QIcon()
        self.disabled_icon.addPixmap(self.gray_img, mode=QIcon.Mode.Disabled, state=QIcon.State.Off)
        self.setIcon(self.icon)
        self.setToolTip(self.NAME)
        self.triggered.connect(self.onclick)

        self.enabled = False
        self.enable()

    def onclick(self):
        raise NotImplementedError

    def cancel(self):
        pass

    def refresh(self, set_enabled):
        if set_enabled:
            self.enable()
        else:
            self.disable()

    def enable(self):
        self.setIcon(self.icon)
        self.enabled = True
        self.setEnabled(True)

    def disable(self):
        self.setIcon(self.disabled_icon)
        self.enabled = False
        self.setEnabled(False)
