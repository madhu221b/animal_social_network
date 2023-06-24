from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHeaderView, QPushButton, QDialogButtonBox, QDialog
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
    def __init__(self):
        super().__init__()
        self.setSizeGripEnabled (True)   

        self.setWindowTitle ('More Network Attributes')
        self.addTableWidget()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        button_box.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

       

    #Create TableWidget 
    def addTableWidget (self) :  
        self.headers = ["Definition of interaction", "Note", "**Citation**"]
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for header_item in self.headers:
            row = self.table.rowCount()
            self.table.insertRow(row)
            item = QTableWidgetItem(header_item)
            item.setFont(QFont('Arial', pointSize=10, weight=QFont.Weight.Bold))
            self.table.setItem(row, 0, item)
            self.table.setItem(row, 1, QTableWidgetItem(PageState.metadata[header_item]))


    # #Allow resizing of QMessageBox
    # def event(self, e):
    #     result = QtGui.QMessageBox.event(self, e)
    #     self.setMinimumWidth(0)
    #     self.setMaximumWidth(16777215)
    #     self.setMinimumHeight(0)
    #     self.setMaximumHeight(16777215)        
    #     self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    #     self.resize(550, 300)
