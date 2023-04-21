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

class SchedulingResultTable(QTableWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        pass

    def initUI(self):
        self.setRowCount(10)
        self.setColumnCount(31)
        self.setHorizontalHeaderLabels([str(i) for i in range(1, 31)])
        self.setVerticalHeaderLabels([str(i) for i in range(1, 11)])

        # Set some data in the table


        self.setItem(0, 0, QTableWidgetItem("Cell 1"))
        self.setItem(0, 1, QTableWidgetItem("Cell 2"))
        self.setItem(0, 2, QTableWidgetItem("Cell 3"))

        self.setItem(1, 0, QTableWidgetItem("Cell 4"))
        self.setItem(1, 1, QTableWidgetItem("Cell 5"))
        self.setItem(1, 2, QTableWidgetItem("Cell 6"))

        self.setItem(2, 0, QTableWidgetItem("Cell 7"))
        self.setItem(2, 1, QTableWidgetItem("Cell 8"))
        self.setItem(2, 2, QTableWidgetItem("Cell 9"))

        self.setItem(3, 0, QTableWidgetItem("Cell 10"))
        self.setItem(3, 1, QTableWidgetItem("Cell 11"))
        self.setItem(3, 2, QTableWidgetItem("Cell 12"))

        # Resize the columns to fit the data
        self.resizeColumnsToContents()
        pass

class Configuration(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

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

        per_grave_label = QLabel("Pergrave")
        per_grave_edit = QLineEdit("10")
        formlayout.addRow(per_grave_label, per_grave_edit)


        n1_label = QLabel("n1")
        n1_edit = QLineEdit("")
        formlayout.addRow(n1_label, n1_edit)


        k_label = QLabel("k")
        k_edit = QLineEdit("")
        formlayout.addRow(k_label, k_edit)

        num_sweeps_label = QLabel("num_sweeps")
        num_sweeps_edit = QLineEdit("")
        formlayout.addRow(num_sweeps_label, num_sweeps_edit)

        year_label = QLabel("year")
        year_edit = QLineEdit("")
        formlayout.addRow(year_label, year_edit)

        month_label = QLabel("month")
        month_edit = QLineEdit("")
        formlayout.addRow(month_label, month_edit)

        lmda_label = QLabel("lmda")
        lmda_edit = QLineEdit("")
        formlayout.addRow(lmda_label, lmda_edit)

        lmdb_label = QLabel("lmdb")
        lmdb_edit = QLineEdit("")
        formlayout.addRow(lmdb_label, lmdb_edit)


        lmdc_label = QLabel("lmdc")
        lmdc_edit = QLineEdit("")
        formlayout.addRow(lmdc_label, lmdc_edit)

        lmde_label = QLabel("lmde")
        lmde_edit = QLineEdit("")
        formlayout.addRow(lmde_label, lmde_edit)

        lmdd_label = QLabel("lmdd")
        lmdd_edit = QLineEdit("")
        formlayout.addRow(lmdd_label, lmdd_edit)

        runbutton = QPushButton("Run")
        formlayout.addRow(runbutton)

        # formlayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.setLayout(formlayout)


class ConfigurationAndResult(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.initUI()

    def initUI(self):

        layout = QGridLayout()
        self.form = Configuration()

        self.table = SchedulingResultTable()


        layout.setColumnStretch(0, 2)
        layout.addWidget(self.form,  0, 1)
        layout.addWidget(self.table, 0, 0)
        self.setLayout(layout)
        pass

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
        self.setWindowTitle("Form Widget")


    def addANewTab(self):
        self.number_of_untitled_tabs += 1
        new_tab = self.createATab("Untitiled" + str(self.number_of_untitled_tabs))
        self.tabwidget.addTab(new_tab, new_tab.name)


    def createATab(self, name):
        tab = ConfigurationAndResult(name)
#        tab = MyWidget(name)
        return tab


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        configuration = SchedulingConfiguration()
        self.setCentralWidget(configuration)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+t")
        new_action.triggered.connect(configuration.addANewTab)


        open_action = QAction("Open", self)

        fileMenu.addActions([new_action, open_action])

        saveMenu = QMenu("Save")
        save_all_action = QAction("Save All", self)
        save_action = QAction("Save", self)

        saveMenu.addActions([save_all_action, save_action])
        fileMenu.addMenu(saveMenu)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
