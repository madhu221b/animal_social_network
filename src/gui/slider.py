import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QFormLayout
from PyQt5.QtCore import Qt


class BSlider(QWidget):
    def __init__(self, title=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.setWindowTitle('PyQt QSlider')
        self.setMinimumWidth(200)

        # create a grid layout
        layout = QFormLayout()
        self.setLayout(layout)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.setSingleStep(5)
        slider.setPageStep(10)
        self.title = title
        slider.setTickPosition(QSlider.TickPosition.TicksAbove)

        slider.valueChanged.connect(self.update2)

        self.result_label = QLabel(f'{self.title}:', self)

        layout.addRow(slider)
        layout.addRow(self.result_label)

        # show the window
        self.show()

    def update2(self, value):
        self.result_label.setText(f'{self.title}: {value}')

class CSlider(QWidget):
    def __init__(self, title=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.setWindowTitle('PyQt QSlider')
        self.setMinimumWidth(200)

        # create a grid layout
        layout = QFormLayout()
        self.setLayout(layout)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.setSingleStep(5)
        slider.setPageStep(10)
        self.title = title
        slider.setTickPosition(QSlider.TickPosition.TicksAbove)

        slider.valueChanged.connect(self.update)

        self.result_label = QLabel(f'{self.title}:', self)

        layout.addRow(slider)
        layout.addRow(self.result_label)

        # show the window
        self.show()

    def update(self, value):
        self.result_label.setText(f'{self.title}: {value}')
