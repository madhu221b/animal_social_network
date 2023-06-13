from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)


class AddNodeForm(QDialog):

    def __init__(self, animal, features):
        super(AddNodeForm, self).__init__()

        self.features = features
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(f"Add a new {animal} node")
        
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("")
        layout = QFormLayout()

        # extract the dict of just 1 entry to extract form labels and the datatype of the value
        label2type = {}
        for _, data in self.features.items():
            label2type = {key:type(val) for key, val in data.items()}
            break 
             
        for form_label, val_type in label2type.items():
            if "str" in str(val_type): # it is a dropdown
                 dropdown = QComboBox()
                 list_of_vals = set([ data[form_label] for _, data in self.features.items()])
                 dropdown.addItems(list_of_vals)
                 layout.addRow(QLabel(form_label), dropdown)
            else: 
                pass   # to do as other data types come
              
        # layout.addRow(QLabel("Age:"), QSpinBox())
        self.formGroupBox.setLayout(layout)