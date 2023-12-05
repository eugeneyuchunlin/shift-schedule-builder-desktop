import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, 
    QLabel, QPushButton, QComboBox,
    QDialog, QVBoxLayout, QHBoxLayout,
    QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ShiftRequirementTagBase(QWidget):
    
    def __init__(self, text, name):
        super().__init__()
        self.name = name
        self.dialog = ShiftRequirementBase(text)



        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 5, 10)
        self.btn = QPushButton(text)
        self.btn.clicked.connect(self.openDialog)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                color: black;
                border: none;
                color: black;
            }

            QPushButton:hover {
                background-color: #ddd;
            }
        """)
        self.setFont(QFont("Arial", 6))

    def openDialog(self):
        self.dialog.exec()
        pass

    def getParameters(self):
        return {
            "name": self.name,
            'parameters' : self.dialog.getParameters()
        }

class ShiftRequirementTagWithWeight(ShiftRequirementTagBase):
    def __init__(self, text, name):
        super().__init__(text, name)
        self.dialog = ShiftRequirementWithWeight(text)

class ShiftRequirementTagWithWeightAndParam(ShiftRequirementTagBase):
    def __init__(self, text, name, param_name):
        super().__init__(text, name)
        self.dialog = ShiftRequirementWithWeightAndParam(text, param_name)


class ShiftRequirementBase(QDialog):

    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        
        self.layout = QFormLayout()
        self.weight_text = QLabel("Weight")
        self.weight_edit = QLineEdit()
        self.layout.addRow(self.weight_text, self.weight_edit)
        self.setLayout(self.layout)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.added)

    def getParameters(self):
        return { "weight" : self.weight_edit.text()}
    
    def added(self):
        self.close()

class ShiftRequirementWithWeight(ShiftRequirementBase):

    def __init__(self, title, ):
        super().__init__(title)
        self.layout.addRow(self.add_button)


class ShiftRequirementWithWeightAndParam(ShiftRequirementBase):

    def __init__(self, title, param_name):
        super().__init__(title)
        self.param_name = param_name
        self.text = QLabel(title)
        self.edit = QLineEdit()
        self.layout.addRow(self.text, self.edit)
        self.layout.addRow(self.add_button)

    def getParameters(self):
        parameters = super().getParameters()
        parameters[self.param_name] = self.edit.text()
        return parameters


class TagBox(QWidget):

    def __init__(self, requirements):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(-1, 0, -1, -1)
        self.layout.addWidget(requirements[0], 0, 0)
        self.layout.addWidget(requirements[1], 1, 0)
        self.layout.addWidget(requirements[2], 2, 0)
        self.layout.addWidget(requirements[3], 3, 0)
        self.layout.addWidget(requirements[4], 0, 1)
        self.layout.addWidget(requirements[5], 2, 1)
        self.layout.addWidget(requirements[6], 1, 1)
        self.setLayout(self.layout)

class ParametersForm(QWidget):
    """
    This class is used to create a form for user to input the parameters of the algorithm.

    ParametersForm is a subclass of QWidget class and it provides the following methods:
        - initUI: create the form
        - parameters: return the parameters of the algorithm
        - toDataFrame: convert the parameters to a pandas dataframe
        - loadParameters: load the parameters from a pandas dataframe

    Attributes:
        parameters_fields: a dictionary of the parameters that contains the name of the parameter as the key
                           and the default value of the parameter as the value
    """
    def __init__(self):
        """
        This is the constructor of the ParametersForm class. It calls the constructor of the QWidget class.
        You can specify the parameters' fields and their default values of the algorithm by setting the parameter_fields argument.
        """
        super().__init__()


        self.initUI()

    def initUI(self):
        """
        This method creates the form for user to input the parameters of the algorithm.
        The fields of the form are created dynamically based on the parameters_fields attribute.
        """
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #495057;
            }

            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                width: 100px;
                background-color: #ffffff;
            }

            QPushButton {
                background-color: #007bff;
                color: #f0f0f0;
                border: none;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QComboBox {
                padding: 6px 12px;
                font-size: 14px;
                line-height: 1.42857143;
                color: #555555;
                background-color: #ffffff;
                background-image: none;
                border: 1px solid #cccccc;
                border-radius: 4px;
                width: 100px;
            }

            QComboBox:hover, QComboBox:focus {
                border-color: #999999;
            }

            QComboBox::drop-down {
                background-color: #ffffff;
            }

            QComboBox::drop-down:hover {
                background-color: #e6e6e6;
            }                    
        """)
        
        layout = QGridLayout()

        self._days_key = QLabel("Days")
        layout.addWidget(self._days_key, 0, 0)

        self._days_edit = QLineEdit("30")
        layout.addWidget(self._days_edit, 0, 1)

        self._number_of_workers = QLabel("Number of workers")
        layout.addWidget(self._number_of_workers, 1, 0)

        self._number_of_workers_edit = QLineEdit("10")
        layout.addWidget(self._number_of_workers_edit, 1, 1)

        self._computation_time = QLabel("Computation time")
        layout.addWidget(self._computation_time, 2, 0)
        self._computation_time_edit = QLineEdit("1")
        layout.addWidget(self._computation_time_edit, 2, 1)

        self.combo = QComboBox()
        self.combo.addItem("DAU")
        self.combo.addItem("SA")

        layout.addWidget(QLabel("Choose a running mode"), 3, 0)
        layout.addWidget(self.combo, 3, 1)

        self.requirements = []
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Expected Number Of Working Days", "expected_number_of_working_days", 'ewd'))
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Expected Number Of Workers Per Shift", "expected_number_of_workers_per_shift", "enwps"))
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Maximum Number Of Consecutive Shifts", "maximum_consecutive_working_days", "mcwd"))
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Minimum Number N Days Off Within 7 Days", "minimum_n_days_leave_within_7_days", "mndlw7d"))
        self.requirements.append(ShiftRequirementTagWithWeight("Successive Shift Pair", "successive_shift_pair"))
        self.requirements.append(ShiftRequirementTagWithWeight("Consecutive Leave", "consecutive_2_days_leave"))
        self.requirements.append(ShiftRequirementTagWithWeight("No Consecutive Leave", "no_consecutive_leave"))
        self.tagBox = TagBox(self.requirements)


        layout.addWidget(QLabel("Constraints"), 4, 0, 1, 2)
        layout.addWidget(self.tagBox, 5, 0, 1, 2)

        self.runbutton = QPushButton("Run")
        self.runbutton.setStyleSheet("""
            QPushButton {
                font-size : 16px;
                padding: 8px 16px;
            }
        """)
        layout.addWidget(self.runbutton, 6, 0, 1, 2)

        self.setLayout(layout)

    def parameters(self) -> dict:
        """
        This method returns the parameters input in the form for the algorithm.

        Returns:
            a dictionary of the parameters
        """
        parameters = []
        for requirement in self.requirements:
            requirement_parameter = requirement.getParameters()
            # check if the requirement is empty
            empty = False
            for key in requirement_parameter['parameters']:
                if requirement_parameter['parameters'][key] == '':
                    empty = True
            if not empty:
                parameters.append(requirement.getParameters())

        data = {
            "type" : self.combo.currentText(),
            "days": int(self._days_edit.text()),
            "number_of_workers": int(self._number_of_workers_edit.text()),
            "computation_time": int(self._computation_time_edit.text()),
            "reserved_leave" : [],
            "constraints" : parameters
        }
        return data
