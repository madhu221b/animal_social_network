from PyQt6.QtWidgets import (QComboBox,
                             QSpinBox,
                             QDoubleSpinBox,
                             QDialog,
                             QDialogButtonBox,
                             QFormLayout,
                             QGroupBox,
                             QLabel,
                             QVBoxLayout)
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AddNodeForm(QDialog):

    # signal = pyqtSignal(tuple)

    def __init__(self, features, callback):
        super().__init__()
        self.features = features
        self.callback = callback
        self.form = {}
        self.new_node = None

        self.create_form_group_box()

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.send)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle(f"Add a new node")

    def create_form_group_box(self):
        self.form_group_box = QGroupBox("")
        layout = QFormLayout()

        # extract the dict of just 1 entry to extract form labels and the datatype of the value
        random_item = list(self.features.values())[0]
        label2type = {key: type(val) for (key, val) in random_item.items()}

        for form_label, val_type in label2type.items():
            print(str(val_type))
            if "str" in str(val_type):  # it is a dropdown
                dropdown = QComboBox()
                list_of_vals = set([data[form_label] for _, data in self.features.items()])
                dropdown.addItems(list_of_vals)
                dropdown.setCurrentIndex(0)
                layout.addRow(QLabel(form_label), dropdown)
                self.form[form_label] = dropdown
            elif "int" in str(val_type):
                spinbox = QSpinBox()
                vals = [data[form_label] for _, data in self.features.items()]
                spinbox.setMinimum(min(vals))
                spinbox.setMaximum(max(vals))
                spinbox.setSingleStep(1)
                spinbox.setValue(vals[0])
                layout.addRow(QLabel(form_label), spinbox)
                self.form[form_label] = spinbox  
            elif  "float" in str(val_type):
                spinbox = QDoubleSpinBox()
                vals = [data[form_label] for _, data in self.features.items()]
                spinbox.setMinimum(min(vals))
                spinbox.setMaximum(max(vals))
                spinbox.setSingleStep(0.1)
                spinbox.setValue(vals[0])
                layout.addRow(QLabel(form_label), spinbox)
                self.form[form_label] = spinbox
            else:
                pass  # to do as other data types come

        # layout.addRow(QLabel("Age:"), QSpinBox())
        self.form_group_box.setLayout(layout)

    def send(self):
        node_data = {k: v.currentText() for (k, v) in self.form.items()}
        self.callback(node_data=node_data)
        self.close()