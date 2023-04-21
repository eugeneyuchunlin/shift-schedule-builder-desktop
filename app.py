# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QTableView, QGridLayout, QFormLayout, QLabel, QLineEdit
from PySide6.QtGui import QAction, QStandardItemModel
from PySide6.QtCore import Qt

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

import calendar

class ShiftTable(QTableWidget):

    def __init__(self, empty_table=True, number_of_rows=None, year=None, month=None):
        super().__init__()

    def createShiftTable(self, number_of_people, year, month):
        days = calendar.monthrange(year, month)[1] # Handle the exception !!

        self.setRowCount(number_of_people)
        self.setColumnCount(days)
        self.setHorizontalHeaderLabels([str(i) for i in range(1, days+1)])
        self.setVerticalHeaderLabels([str(i) for i in range(1, number_of_people + 1)])
        self.resizeColumnsToContents()


    def loadShiftTable(self):
        pass

    def setShiftTable(self):
        pass

class Configuration(QWidget):

    def __init__(self, table:ShiftTable):
        super().__init__()
        self.initUI()
        self._table = table

    def initUI(self):
#        per_grave = 10 #m1
#        n1 = 7
#        ## k: the max number of consecutive graveyard shifts and of consecutive night shifts
#        k = 5
#        num_sweeps = 150000
#        year = 2022
#        month = 9
#        lmda = 1.5
#        lmdb = 0.5
#        lmdc = 0.5
#        lmde = 0.5
#        lmdd = 0.1

        formlayout = QFormLayout()

        self.per_grave_label = QLabel("Pergrave")
        self.per_grave_edit = QLineEdit()
        formlayout.addRow(self.per_grave_label, self.per_grave_edit)
        self.per_grave_edit.editingFinished.connect(self._generateNewMonthTable)


        self.n1_label = QLabel("n1")
        self.n1_edit = QLineEdit("")
        formlayout.addRow(self.n1_label, self.n1_edit)


        self.k_label = QLabel("k")
        self.k_edit = QLineEdit("")
        formlayout.addRow(self.k_label, self.k_edit)

        self.num_sweeps_label = QLabel("num_sweeps")
        self.num_sweeps_edit = QLineEdit("")
        formlayout.addRow(self.num_sweeps_label, self.num_sweeps_edit)

        self.year_label = QLabel("year")
        self.year_edit = QLineEdit("")
        formlayout.addRow(self.year_label, self.year_edit)
        self.year_edit.editingFinished.connect(self._generateNewMonthTable)


        self.month_label = QLabel("month")
        self.month_edit = QLineEdit("")
        formlayout.addRow(self.month_label, self.month_edit)
        self.month_edit.editingFinished.connect(self._generateNewMonthTable)

        self.lmda_label = QLabel("lmda")
        self.lmda_edit = QLineEdit("")
        formlayout.addRow(self.lmda_label, self.lmda_edit)

        self.lmdb_label = QLabel("lmdb")
        self.lmdb_edit = QLineEdit("")
        formlayout.addRow(self.lmdb_label, self.lmdb_edit)


        self.lmdc_label = QLabel("lmdc")
        self.lmdc_edit = QLineEdit("")
        formlayout.addRow(self.lmdc_label, self.lmdc_edit)

        self.lmde_label = QLabel("lmde")
        self.lmde_edit = QLineEdit("")
        formlayout.addRow(self.lmde_label, self.lmde_edit)

        self.lmdd_label = QLabel("lmdd")
        self.lmdd_edit = QLineEdit("")
        formlayout.addRow(self.lmdd_label, self.lmdd_edit)

        runbutton = QPushButton("Run")
        formlayout.addRow(runbutton)

        self.setLayout(formlayout)

    def _generateNewMonthTable(self):
        # check data
        year = self.year_edit.text()
        month = self.month_edit.text()
        number_of_people = self.per_grave_edit.text()

        if year.isdigit() and len(year) > 0:
            year = int(year)
        else:
            return
        if month.isdigit() and len(month) > 0:
            month = int(month)
        else:
            return
        if number_of_people.isdigit() and len(number_of_people) > 0:
            number_of_people = int(number_of_people)
        else:
            return

        self._table.createShiftTable(number_of_people, year, month)
        pass

class ConfigurationAndResult(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.initUI()

    def initUI(self):

        layout = QGridLayout()
        self.table = ShiftTable()
        self.form = Configuration(self.table)

        layout.setColumnStretch(0, 2)
        layout.addWidget(self.form,  0, 1)
        layout.addWidget(self.table, 0, 0)
        self.setLayout(layout)

    def setMonth(self, month):
        self._month = month

    def setYear(self, year):
        self._year = year



class SchedulingConfiguration(QWidget):
    def __init__(self):
        super().__init__()

        self.number_of_untitled_tabs = 0
        self.names = []

        self.initUI()

    def initUI(self):
        self.tabwidget = QTabWidget()

        self.addANewTab()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabwidget)

        self.setLayout(vbox)


    def addANewTab(self):
        self.number_of_untitled_tabs += 1
        new_tab = self.createATab("Untitiled" + str(self.number_of_untitled_tabs))
        self.tabwidget.addTab(new_tab, new_tab.name)


    def createATab(self, name):
        tab = ConfigurationAndResult(name)
        return tab

    def switchToLastTab(self):
        self.tabwidget.setCurrentIndex(self.number_of_untitled_tabs - 1)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.configuration = SchedulingConfiguration()
        self.setCentralWidget(self.configuration)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+t")
        new_action.triggered.connect(self.newTabTrigger)


        open_action = QAction("Open", self)


        saveMenu = QMenu("Save")
        save_all_action = QAction("Save All", self)
        save_action = QAction("Save", self)



        seperator_action = QAction("", self)
        seperator_action.setSeparator(True)
        export = QAction("Export", self)



        fileMenu.addActions([new_action, open_action])
        saveMenu.addActions([save_all_action, save_action])
        fileMenu.addMenu(saveMenu)
        fileMenu.addActions([seperator_action, export])

    def newTabTrigger(self):
        self.configuration.addANewTab()
        self.configuration.switchToLastTab()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
