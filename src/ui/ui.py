# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QPushButton,
    QTabWidget, QTableWidget, QMenu,
    QVBoxLayout, QLabel, QLineEdit,
    QGridLayout, QFormLayout, QTableWidgetItem,
    QHBoxLayout,
    QTextEdit, QFileDialog, QDialog, QComboBox
)
from PySide6.QtGui import QAction
import pandas as pd
from .parameters import SA_FORM_CONFIG, DAU_FORM_CONFIG
from ..utility.util import getFileName

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from .ui_form import Ui_MainWindow

import calendar

from src.ui.login import LoginDialog
from src.ui.table_widget import TableWidget
from src.ui.shift_table import ShiftTable



class AlgorithmData(TableWidget):
    """
    This class is used to create a table widget to display the algorithm data

    AlgorithmData is a subclass of TableWidget class.
    """

    def __init__(self):
        super().__init__()


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

    def __init__(self, running_mode: str = None):
        """
        This is the constructor of the ParametersForm class. It calls the constructor of the QWidget class.
        You can specify the parameters' fields and their default values of the algorithm by setting the parameter_fields argument.
        """
        super().__init__()

        self._running_mode = running_mode

        if self._running_mode is None:
            self.parameters_fields = DAU_FORM_CONFIG
        else:
            if self._running_mode == 'DAU':
                self.parameters_fields = DAU_FORM_CONFIG
            elif self._running_mode == 'SA':
                self.parameters_fields = SA_FORM_CONFIG

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

    def __init__(self, name: str, running_mode: str):
        """
        This is the constructor of the WorkingArea class. It calls the constructor of the QWidget class.
        You can specify the name of the working area by setting the name argument.

        """
        super().__init__()

        self.name = name
        self.running_mode = running_mode

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
        self.form = ParametersForm(self.running_mode)

        # connect the signal of edit fields
        self.form._number_of_workers_edit.editingFinished.connect(
            self.generateEmptyShift)
        self.form._days_edit.editingFinished.connect(self.generateEmptyShift)

        self.generateEmptyShift()

        self.algorithm_table = AlgorithmData()

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


class Tabs(QWidget):
    """
    This class is used to create a tab widget and handle tabs.

    The tab widget contains the following components:
        - a tab widget
        - a list of tabs
        - a list of names of the tabs

    The tab widget is a subclass of QWidget class and it provides the following methods:
        - initUI: create the tab widget
        - addANewTab: add a new tab to the tab widget
        - createATab: create a new tab
        - switchToLastTab: switch to the last tab
        - exportWorkingArea: export the working area to a three dataframes
        - currentTab: get the current tab
        - setCurrentTabName: set the name of the current tab

    Attributes:
        configuration_type: the type of the tab
        number_of_untitled_tabs: the number of untitled tabs
        tabwidget: the tab widget
        tabs: the list of tabs
        names: the list of names of the tabs
    """

    tabs = []
    names = []

    def __init__(self, configurationType: QWidget, mode: str):
        """
        This is the constructor of the Tabs class. It calls the constructor of the QWidget class.
        You can specify the type of the tab by setting the configurationType argument.

        """
        super().__init__()

        self.number_of_untitled_tabs = 0  # FIXME: deprecated

        self.configuration_type = configurationType

        self.initUI(mode)

    def initUI(self, init_mode):
        """
        This method initializes the ui and creates the tab widget.
        """
        self.tabwidget = QTabWidget()

        self.addANewTab(init_mode)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabwidget)

        self.setLayout(vbox)

    def addANewTab(self, mode: str):
        """
        This method adds a new tab to the tab widget.
        """

        self.number_of_untitled_tabs += 1
        new_tab = self.createATab(
            "Untitiled" + str(self.number_of_untitled_tabs), mode)
        self.tabs.append(new_tab)
        self.tabwidget.addTab(new_tab, new_tab.name)

    def createATab(self, name: str, mode: str) -> QWidget:
        """
        This method creates a new tab.
        """
        tab = self.configuration_type(name, mode)
        return tab

    def switchToLastTab(self):
        """
        This method switches to the last tab.
        """
        self.tabwidget.setCurrentIndex(self.number_of_untitled_tabs - 1)

    def exportWorkingArea(self) -> tuple:
        """
        This method exports the working area to a three dataframes.

        Returns:
            A tuple of three dataframes: the shift table, the algorithm table, and the form.
        """
        working_area = self.tabs[self.tabwidget.currentIndex()]
        return working_area.table.exportTableToDataFrame(
        ), working_area.algorithm_table.exportTableToDataFrame(), working_area.form.toDataFrame()

    def currentTab(self) -> QWidget:
        """
        This method gets the current tab.

        Returns:
            The current tab in QWidget type.
        """
        return self.tabs[self.tabwidget.currentIndex()]

    def setCurrentTabName(self, new_name: str):
        """
        This method sets the name of the current tab.

        Args:
            new_name: the new name of the current tab
        """
        self.tabwidget.setTabText(self.tabwidget.currentIndex(), new_name)


class RunningModeDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Choose a running mode")

        dialog_layout = QVBoxLayout()

        formlayout = QFormLayout()
        self.combo = QComboBox()
        self.combo.addItem("DAU")
        self.combo.addItem("SA")

        formlayout.addRow(QLabel("Choose a running mode"), self.combo)
        dialog_layout.addLayout(formlayout)
        okbtn = QPushButton("OK")
        okbtn.clicked.connect(self.okBtnClicked)
        dialog_layout.addWidget(okbtn)

        self.setLayout(dialog_layout)

    def mode(self):
        return self._mode

    def okBtnClicked(self):
        self._mode = self.combo.currentText()
        self.close()


class MainWindow(QMainWindow):
    # TODO: finish the documentation
    """
    This class is used to create the main window of the application.
    """

    def __init__(self, Configuration, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Shift Generator")

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+t")
        new_action.triggered.connect(self.newTabTrigger)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.openFile)
        open_action.setShortcut("Ctrl+o")
        open_action.setEnabled(False)

        saveMenu = QMenu("Save")
        save_all_action = QAction("Save All", self)
        save_all_action.setEnabled(False)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+s")
        save_action.triggered.connect(self.saveFile)

        seperator_action = QAction("", self)
        seperator_action.setSeparator(True)

        export = QAction("Export", self)
        export.setEnabled(False)

        fileMenu.addActions([new_action, open_action])
        saveMenu.addActions([save_all_action, save_action])
        fileMenu.addMenu(saveMenu)
        fileMenu.addActions([seperator_action, export])

        # insert the login dialog here

        self.configuration = Tabs(
            Configuration, self.chooseRunningModeDialog())
        self.setCentralWidget(self.configuration)

    def saveFile(self):
        current_tab = self.configuration.currentTab()

        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save File', current_tab.name, 'Excel (*.xlsx);;All Files (*.*)')

        # If the user cancels the save file dialog, return
        if not file_path:
            return

        df_shift, df_algorithm_data, df_form = self.configuration.exportWorkingArea()

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df_shift.to_excel(writer, sheet_name="shift")
            df_algorithm_data.to_excel(writer, sheet_name="data")
            df_form.to_excel(writer, sheet_name="parameters")

        self.configuration.setCurrentTabName(getFileName(file_path))

    def openFile(self):

        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '.', ("Excel (*xlsx *xls)"))
        try:
            df_shift = pd.read_excel(
                filename, sheet_name="shift", index_col=0, dtype=str)
            df_algorithm_data = pd.read_excel(
                filename, sheet_name="data", index_col=0, dtype=str)
            df_form = pd.read_excel(
                filename,
                sheet_name="parameters",
                index_col=0,
                dtype=str)
        except BaseException:
            pass

        tab = self.configuration.currentTab()
        tab.algorithm_table.loadDataFrame(df_algorithm_data)
        tab.table.loadDataFrame(df_shift)

        tab.form.loadParametersFromDataFrame(df_form)

        self.configuration.setCurrentTabName(getFileName(filename))

    def chooseRunningModeDialog(self):

        dialog = RunningModeDialog()

        dialog.exec()
        return dialog.mode()

    def newTabTrigger(self):
        mode = self.chooseRunningModeDialog()
        self.configuration.addANewTab(mode)
        self.configuration.switchToLastTab()

    def closeEvent(self, event):
        event.accept()
        pass
