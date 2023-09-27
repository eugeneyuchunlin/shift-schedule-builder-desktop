from PySide6.QtWidgets import (QWidget, QGridLayout, QTextEdit)
from .shift_table import ShiftTable
from .parameters_form import ParametersForm

class WorkingArea(QWidget):
    """
    This class is used to create a working area for the algorithm.

    The working area contains the following components:
        - a shift table
        - a form for user to input the parameters of the algorithm
        - a table to display the algorithm data
        - a log to display the log of the algorithm

    The working area is a subclass of QWidget class and it provides the following methods:
        - initUI: create the working area
        - generateEmptyShift: generate an empty shift table

    Attributes:
        name: the name of the working area
        running_thread: the thread that runs the algorithm
        table: the shift table
        form: the form for user to input the parameters of the algorithm
        algorithm_table: the table to display the algorithm data
        log: the log to display the log of the algorithm
    """

    def __init__(self, name: str):
        """
        This is the constructor of the WorkingArea class. It calls the constructor of the QWidget class.
        You can specify the name of the working area by setting the name argument.

        """
        super().__init__()

        self.name = name

        self.running_thread = None

        self.initUI()

    def initUI(self):
        """
        This method creates the working area.

        The working area contains the following components:
            - a shift table
            - a form for user to input the parameters of the algorithm
            - a table to display the algorithm data
            - a log to display the log of the algorithm
        """
        layout = QGridLayout()
        self.table = ShiftTable()
        self.form = ParametersForm()

        # connect the signal of edit fields
        self.form._number_of_workers_edit.editingFinished.connect(
            self.generateEmptyShift)
        self.form._days_edit.editingFinished.connect(self.generateEmptyShift)

        self.generateEmptyShift()

        # self.algorithm_table = AlgorithmData()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.table, 0, 0, 3, 1)
        layout.addWidget(self.form, 0, 1, 2, 2)
        # layout.addWidget(self.algorithm_table, 1, 0)
        # layout.addWidget(self.log, 2, 0)

        self.setLayout(layout)

    def generateEmptyShift(self):
        """
        This method generates an empty shift table based on the parameters input in the form.

        The method is used as a slot of the signal of the edit fields of the form; thus, when user
        changes the parameters in the form, especially the fields, the per_grave, the year, and the month,
        the method will generate an empty shift table based on the parameters input in the form.
        """

        # FIXME: The method should should the data
        number_of_people = self.form._number_of_workers_edit.text()
        number_of_days = self.form._days_edit.text()
        
        if number_of_people.isdigit() and len(number_of_people) > 0:
            number_of_people = int(number_of_people)
        else:
            return

        if number_of_days.isdigit() and len(number_of_days) > 0:
            number_of_days = int(number_of_days)

        self.table.createShiftTable(number_of_people, days=number_of_days)

