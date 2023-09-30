import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, 
    QLabel, QPushButton, QComboBox,
    QDialog, QHBoxLayout
)


class ShiftRequirementTagBase(QWidget):
    
    def __init__(self, text, name):
        super().__init__()
        self.name = name
        self.dialog = ShiftRequirementBase(text)

        self.layout = QFormLayout()
        self.btn = QPushButton(text)
        self.btn.clicked.connect(self.openDialog)
        self.layout.addRow(self.btn)
        self.setLayout(self.layout)

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
        formlayout = QFormLayout()

        self._days_key = QLabel("Days")
        self._days_edit = QLineEdit("30")
        formlayout.addRow(self._days_key, self._days_edit)

        self._number_of_workers = QLabel("Number of workers")
        self._number_of_workers_edit = QLineEdit("10")
        formlayout.addRow(self._number_of_workers, self._number_of_workers_edit)

        self._computation_time = QLabel("Computation time")
        self._computation_time_edit = QLineEdit("1")
        formlayout.addRow(self._computation_time, self._computation_time_edit)

        self.combo = QComboBox()
        self.combo.addItem("DAU")
        self.combo.addItem("SA")

        formlayout.addRow(QLabel("Choose a running mode"), self.combo)

        self.requirements = []
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Expected Number Of Working Days", "expected_number_of_working_days", 'ewd'))
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Expected Number Of Workers Per Shift", "expected_number_of_workers_per_shift", "enwps"))
        self.requirements.append(ShiftRequirementTagWithWeight("Successive Shift Pair", "successive_shift_pair"))
        self.requirements.append(ShiftRequirementTagWithWeight("Consecutive 2 Days Off", "consecutive_2_days_leave"))
        self.requirements.append(ShiftRequirementTagWithWeight("No More Than 2 Consecutive Days Off", "no_consecutive_leave"))
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Maximum Number Of Consecutive Shifts", "maximum_consecutive_working_days", "mcwd"))
        self.requirements.append(ShiftRequirementTagWithWeightAndParam("Minimum Number N Days Off Within 7 Days", "minimum_n_days_leave_within_7_days", "mndlw7d"))

        for requirement in self.requirements:
            formlayout.addRow(requirement)

        self.runbutton = QPushButton("Run")
        formlayout.addRow(self.runbutton)

        self.setLayout(formlayout)

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
            "shift_id" : "123",
            "reserved_leave" : [],
            "constraints" : parameters
        }
        return data

    def toDataFrame(self) -> pd.DataFrame:
        """
        This method converts the parameters to a pandas dataframe.
        The DataFrame will have only one row.
        For example:

            per_grave  n1  k  num_sweeps  year  month  lmda  lmdb  lmdc  lmdd  lmde
        0         10   7  5      150000   2022      9   1.5   0.5   0.5   0.1   0.5

        Returns:
            a pandas dataframe of the parameters
        """
        form = {}
        for key in self.parameters_fields:
            form[key] = [getattr(self, key + "_edit").text()]

        return pd.DataFrame(form)

    def loadParametersFromDataFrame(self, df: pd.DataFrame):
        """
        This method loads the parameters from a pandas dataframe.

        Args:
            df: a pandas dataframe of the parameters

        deprecated:
            This method is deprecated. Since it only load the first row of the dataframe.
            The bug will be fixed in the next version.
        """
        # FIXME: should check parameter fields that satisfy with the setting
        columns = df.columns
        for col in columns:
            getattr(self, col + "_edit").setText(str(df[col][0]))

    def runningMode(self):
        return self._running_mode

