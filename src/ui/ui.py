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
from src.ui.parameters_form import ParametersForm
from src.ui.tabs import Tabs
from src.model.data_adapter import DataAdapter




class AlgorithmData(TableWidget):
    """
    This class is used to create a table widget to display the algorithm data

    AlgorithmData is a subclass of TableWidget class.
    """

    def __init__(self):
        super().__init__()



class MainWindow(QMainWindow):
    # TODO: finish the documentation
    """
    This class is used to create the main window of the application.
    """

    def __init__(self, parent=None):
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
        self.login_dialog = LoginDialog()
        self.login_dialog.exec()
        
        # if the user cancels the login dialog, close the application
        self.user = self.login_dialog.getUser()
        if self.user is None:
            quit()

        self.configuration = Tabs(self.user)
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

    # def chooseRunningModeDialog(self):

    #     dialog = RunningModeDialog()

    #     dialog.exec()
    #     return dialog.mode()

    def newTabTrigger(self):
        # mode = self.chooseRunningModeDialog()
        self.configuration.addANewTab()
        self.configuration.switchToLastTab()

    def closeEvent(self, event):
        event.accept()
        pass
