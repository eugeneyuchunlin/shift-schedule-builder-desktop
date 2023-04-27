import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Signal
from ui import MainWindow, WorkingArea

from Solver import DAUSolver, SASolver

import pandas as pd
import threading


class NSPSolver(WorkingArea):


    dau_solver = DAUSolver()
    sa_solver = SASolver()

    def __init__(self, name, form_config):
        super().__init__(name, form_config)

        self.form.runbutton.clicked.connect(self.runTrigger)
        self.dau_solver.error.connect(self.errorHandlerSlot)
        self.sa_solver.error.connect(self.errorHandlerSlot)
        self.dau_solver.finished.connect(self.finishRunningSlot)
        self.sa_solver.finished.connect(self.finishRunningSlot)


    def runTrigger(self):
        DAUorSA = self.form.runningMode()
        parameters = self.form.parameters()
        print(parameters)
        if DAUorSA == 'DAU':
            self.dau_solver.setParameters(**parameters)
            self.dau_solver.start()
        else:
            self.sa_solver.setParameters(**parameters)
            self.sa_solver.start()

        self.form.runbutton.setDisabled(True)


    def errorHandlerSlot(self, alert_msg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(alert_msg)
        msg.setWindowTitle("Error")
        msg.addButton(QMessageBox.Ok)
        msg.exec()

        self.form.runbutton.setDisabled(False) 

    def finishRunningSlot(self, shift:pd.DataFrame, algorithm_data:pd.DataFrame):
        self.table.loadDataFrame(shift)
        self.algorithm_table.loadDataFrame(algorithm_data)
        self.form.runbutton.setDisabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver)  # pass type
    win.show()
    sys.exit(app.exec())
