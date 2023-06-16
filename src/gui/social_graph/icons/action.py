import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QPixmap, QImage, qGray


class IconAction(QAction):

    ROOT = "./res/icons"
    NAME = None
    FILENAME = None

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.img = QPixmap(os.path.join(self.ROOT, self.FILENAME))
        self.icon = QIcon()
        self.icon.addPixmap(self.img, QIcon.Normal, QIcon.On)
        self.setIcon(self.icon)
        self.setToolTip(self.NAME)
        self.triggered.connect(self.onclick)

        self.enabled = False
        self.enable()

    def onclick(self):
        raise NotImplementedError
    
    def cancel(self):
        pass

    def refresh(self, active):
        if active:
            self.enable()
        else:
            self.disable()

    def enable(self):
        self.icon.addPixmap(self.img, QIcon.Normal, QIcon.On)
        self.enabled = True

    def disable(self):
        grayed = self.icon.pixmap(self.img.size(), QIcon.Disabled, QIcon.On)
        self.icon.addPixmap(grayed, QIcon.Normal, QIcon.Off)
        self.enabled = False