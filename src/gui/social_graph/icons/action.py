import os
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon, QPixmap, QImage, qGray


class IconAction(QAction):

    ROOT = "./res/icons"
    NAME = None
    FILENAME = None

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.img = QPixmap(os.path.join(self.ROOT, self.FILENAME))
        self.icon = QIcon()
        self.icon.addPixmap(self.img, mode=QIcon.Mode.Normal, state=QIcon.State.On)        
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
        self.icon.addPixmap(self.img, mode=QIcon.Mode.Normal, state=QIcon.State.On)
        self.enabled = True

    def disable(self):
        grayed = self.icon.pixmap(self.img.size(), QIcon.Mode.Disabled, QIcon.State.On)
        self.icon.addPixmap(grayed, mode=QIcon.Mode.Normal, state=QIcon.State.Off)
        self.enabled = False