import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, 
    QLabel, QPushButton, QComboBox,
    QDialog,
)


class ShiftRequirementTag(QPushButton):
    
    def __init__(self, text):
        super().__init__()
        self.setText(text)

    def openDialog(self):
        self.exec()
        pass

class WorkingDays(QDialog):

    def __init__(self, text):
        super().__init__()
        
        self.setWindowTitle(text)

        self.layout = QFormLayout()
        
        self.text = QLabel("Expected Number of Working Days")
        self.edit = QLineEdit()
        self.layout.addRow(self.text, self.edit)

        self.weight_text = QLabel("Weight")
        self.weight_edit = QLineEdit()
        self.layout.addRow(self.weight_text, self.weight_edit)

        self.setLayout(self.layout)
        
        self.button = QPushButton("Add")
        self.layout.addRow(self.button)

    def getWorkingDays(self):
        return self.edit.text(), self.weight_edit.text()

    def openDialog(self):
        self.exec()

    def added(self):

        pass
        


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
        self._number_of_workers_edit = QLineEdit("8")
        formlayout.addRow(self._number_of_workers, self._number_of_workers_edit)

        self._computation_time = QLabel("Computation time")
        self._computation_time_edit = QLineEdit("100")
        formlayout.addRow(self._computation_time, self._computation_time_edit)

        self.combo = QComboBox()
        self.combo.addItem("DAU")
        self.combo.addItem("SA")

        formlayout.addRow(QLabel("Choose a running mode"), self.combo)

        self.sr = QPushButton("Working Days Requirement")

        self.working_days = WorkingDays("Working Days Requirement")

        self.sr.clicked.connect(self.working_days.openDialog)
        formlayout.addRow(self.sr)

        self.runbutton = QPushButton("Run")
        formlayout.addRow(self.runbutton)

        self.setLayout(formlayout)

    def parameters(self) -> dict:
        """
        This method returns the parameters input in the form for the algorithm.

        Returns:
            a dictionary of the parameters
        """
        parameters = {}
        for key in self.parameters_fields:
            parameters[key] = getattr(self, key + "_edit").text()

        return parameters

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

