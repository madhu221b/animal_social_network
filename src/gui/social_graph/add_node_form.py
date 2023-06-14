from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class AddNodeForm(QDialog):

    signal = pyqtSignal(tuple)
    def __init__(self, animal, features):
        super(AddNodeForm, self).__init__()
        self.features = features
        self.animal = animal
        self.form_instances = []
        self.new_node = None
      

        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(f"Add a new {self.animal} node")
        
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
                 dropdown.setCurrentIndex(0)
                 layout.addRow(QLabel(form_label), dropdown)
                 self.form_instances.append({form_label:dropdown})
            else: 
                pass   # to do as other data types come
              
        # layout.addRow(QLabel("Age:"), QSpinBox())
        self.formGroupBox.setLayout(layout)

    
    def accept(self):
        new_node, new_name, new_id  = {}, "", 1
        for form_instance in self.form_instances: 
            key, val = None, None
            for form_label, form_obj in form_instance.items():
                key, val = form_label, form_obj.currentText()
                new_node[key] = val
                break
        # Assign a new name to the node of convention new_<<animal_name>>_id
        names = [node for node, _ in self.features.items() if node.startswith("new")]
      
        if names: # give the last most id
            new_id = int(names.sort()[-1].split("_")[-1])+1

        new_name = "new_{}_{}".format(self.animal, new_id)
        self.new_node = (new_name, new_node)
        self.signal.emit(self.new_node)
        self.hide()

        
