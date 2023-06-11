from PyQt5 import QtCore, QtWidgets
from canvas import Canvas

class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()

class Window(QtWidgets.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        title = "Social Network Analysis of Animals"
        self.setWindowTitle(title)
        self.setGeometry(0, 0, 500, 300)
        self.combo = ComboBox(self)
        self.combo.popupAboutToBeShown.connect(self.populateCombo)
        self.combo.view().pressed.connect(self.handleItemPressed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.combo)

    def populateCombo(self):
        if not self.combo.count():
            list_of_animals = ["Animal1", "Animal2", "Animal3"]
            self.combo.addItems(list_of_animals)

    def handleItemPressed(self, index):
        item = self.combo.model().itemFromIndex(index)
        print("Item Selected:", item.text())
        self.w = Canvas(text=item.text())
        self.w.show()
        self.hide()
      

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())