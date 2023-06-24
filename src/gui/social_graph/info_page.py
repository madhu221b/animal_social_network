from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHeaderView, QPushButton, QDialogButtonBox, QDialog, QPlainTextEdit, QHBoxLayout
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.static import PageState

class InfoPage(QWidget):

    def __init__(self, graph):
        super(InfoPage, self).__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.headers = ["Nodes", "Edges", "Interaction type","Taxonomic class","Population type"]
        self.headers_2 = ["Geographical location", "Data collection technique", 
           "Total duration of data collection", "Time span of data collection (within a day)"]

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setRowCount(1)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 50)

        n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()   
        self.table.setItem(0, 0, QTableWidgetItem(str(n_nodes)))
        self.table.setItem(0, 1, QTableWidgetItem(str(n_edges)))

        for count, header_item in enumerate(self.headers[2:]):
            item = QTableWidgetItem(PageState.metadata[header_item])
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table.setItem(0, count+2, item)
            self.table.horizontalHeader().setSectionResizeMode(count, QHeaderView.ResizeMode.ResizeToContents)
            # self.table.setItem(0, 3, QTableWidgetItem(PageState.metadata["Taxonomic class"]))
            # self.table.setItem(0, 4, QTableWidgetItem(PageState.metadata["Population type"]))
       

        self.table2 = QTableWidget(self)
        self.table2.setColumnCount(len(self.headers_2))
        self.table2.setHorizontalHeaderLabels(self.headers_2)
        self.table2.verticalHeader().setVisible(False)
        self.table2.setRowCount(1)

        for count, header_item in enumerate(self.headers_2):
            item = QTableWidgetItem(PageState.metadata[header_item])
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table2.setItem(0, count, item)
            self.table2.horizontalHeader().setSectionResizeMode(count, QHeaderView.ResizeMode.ResizeToContents)
        
        self.button = QPushButton("More Network Attributes")
        self.button.clicked.connect(self.button_clicked)

        title = "Network Attributes"
        self.label = QLabel(title)
        self.label.setStyleSheet("font-weight: bold")


        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.table2)
        self.layout.addWidget(self.button)

        self.layout.addStretch(1)
    
    def refresh(self,graph):
        n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
        self.table.setItem(0, 0, QTableWidgetItem(str(n_nodes)))
        self.table.setItem(0, 1, QTableWidgetItem(str(n_edges)))
    
    def button_clicked(self):
        info = InfoMessageBox()
        info.exec()


class InfoMessageBox(QDialog):
    def __init__(self, width=600, height=300):
        super().__init__()
        self.setSizeGripEnabled (True)   

        self.setWindowTitle ('More Network Attributes')
        
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        button_box.rejected.connect(self.reject)
        
        self.main_layout = QVBoxLayout()
        self.addTextWidget()
        self.main_layout.addWidget(button_box)

        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.main_layout)

       

    #Create TableWidget 
    def addTextWidget (self) :  
        self.headers = ["Definition of interaction", "Note", "**Citation**"]
        for header in self.headers:
            self.h = QHBoxLayout()
            self.label = QLabel(f"{header}: ")
            self.label.setStyleSheet("font-weight: bold")
            self.b = QPlainTextEdit(self)
            self.b.insertPlainText(f"{PageState.metadata[header]}")
            self.b.setReadOnly(True)
            self.h.addWidget(self.label)
            self.h.addWidget(self.b)
            self.main_layout.addLayout(self.h)


    # #Allow resizing of QMessageBox
    # def event(self, e):
    #     result = QtGui.QMessageBox.event(self, e)
    #     self.setMinimumWidth(0)
    #     self.setMaximumWidth(16777215)
    #     self.setMinimumHeight(0)
    #     self.setMaximumHeight(16777215)        
    #     self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    #     self.resize(550, 300)
