from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.utils.common import swap_dict_keys


class NodeInfoPage(QWidget):

    def __init__(self, features, metrics, title="Features", globalmetrics=True):
        super(NodeInfoPage, self).__init__()

        self.LEFT_WIDTH = 200
        self.RIGHT_WIDTH = 200
        self.CELL_HEIGHT = 30
        self.FEATURES = None
        self.METRICS = None  # None == select all

        self.features = features
        self.metrics = swap_dict_keys(metrics)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.feature_title_label = QLabel(title)
        self.feature_title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.layout.addWidget(self.feature_title_label)

        for _, data in self.features.items():
            self.FEATURES = data.keys()
            break
        self.feature_table = self._create_table(self.features, self.LEFT_WIDTH, self.FEATURES)
        self.layout.addWidget(self.feature_table)

        if globalmetrics:
            self.metric_title_label = QLabel("Metrics")
            self.metric_title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
            self.layout.addWidget(self.metric_title_label)

            self.metric_table = self._create_table(metrics, self.RIGHT_WIDTH, self.METRICS)
            self.layout.addWidget(self.metric_table)

        self.layout.addStretch(1)

    def _create_table(self, data, width, columns=None):
        table = QTableWidget()
        table.setFixedWidth(width)
        table.setColumnCount(2)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Populate the table with titles and dummy values
        columns = columns if columns is not None else list(data.keys())

        # if it is a feature table
        if "betweeness" not in columns:  # first entry of the features table is Name
            columns = list(columns)
            columns.insert(0, "Name")

        for key in columns:
            row = table.rowCount()
            table.insertRow(row)
            item = QTableWidgetItem(f"{key}")
            item.setFont(QFont('Arial', pointSize=10, weight=QFont.Weight.Bold))
            table.setItem(row, 0, item)
            table.setItem(row, 1, QTableWidgetItem(""))

        table.setFixedHeight(self.CELL_HEIGHT * table.rowCount())

        return table

    def update(self, node_name, features=None, metrics=None):

        if node_name:
            self.features = features
            self.metrics = swap_dict_keys(metrics)
            self._update_table(self.feature_table, self.features[node_name], node_name=node_name)
            self._update_table(self.metric_table, self.metrics[node_name])

    def _update_table(self, table, data, node_name=None):
        for row in range(table.rowCount()):
            key_item = table.item(row, 0)
            if node_name and key_item.text().lower() == "name":
                value = node_name
            else:
                value = data.get(key_item.text(), "")
            value = f"{value:.2f}" if isinstance(value, float) else value
            item = QTableWidgetItem(str(value))
            table.setItem(row, 1, item)