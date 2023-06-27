from PyQt6.QtWidgets import QPushButton
from PyQt6 import QtCore


class GreenButton(QPushButton):

    id = 0

    def __init__(self, *args, font_size=16, font_weigth='bold', padding="10px 20px", **kwargs):
        super().__init__(*args, **kwargs)

        self.id = GreenButton.id
        GreenButton.id += 1
        self.setObjectName(f"{self.id}")

        # Set button properties and styles
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f'''
            QPushButton#{self.id} {{
                background-color: #3C8F40;
                color: white;
                padding: {padding};
                font-weight: {font_weigth};
                font-size: {str(int(font_size))}px;
            }}
            
            QPushButton#{self.id}:hover {{
                background-color: #4CAF50;
            }}
            ''')


class SmallGreenButton(GreenButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, font_size=12, padding="5px 10px", **kwargs)


class MediumGreenButton(GreenButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, font_size=14, padding="10px 20px", **kwargs)


class LargeGreenButton(GreenButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, font_size=16, padding="10px 20px", **kwargs)


class BlueArrowButton(QPushButton):

    id = 0

    def __init__(self,
                 *args,
                 font_size=16,
                 font_weigth='bold',
                 padding="10px 20px",
                 size=32,
                 icon_size=32,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.id = BlueArrowButton.id
        BlueArrowButton.id += 1
        self.setObjectName(f"{self.id}")

        self.setFixedWidth(size)
        self.setFixedHeight(size)
        self.setIconSize(QtCore.QSize(icon_size, icon_size))

        # Set button properties and styles
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f'''
            QPushButton#{self.id} {{
                background-color: #3C8F40;
                color: white;
                padding: {padding};
                font-weight: {font_weigth};
                font-size: {str(int(font_size))}px;
                border-radius: {self.height() // 2}px; 
            }}
            
            QPushButton#{self.id}:hover {{
                background-color: #4CAF50; 
            }}

            QPushButton#{self.id}:disabled {{
                background-color: #bbbbbb;
            }}
        ''')