import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ui import MainWindow, WorkingArea

from Solver import DAUSolver, SASolver

import pandas as pd
import os


class NSPSolver(WorkingArea):

    # TODO: enable user to register new solver
    def __init__(self, name, mode):
        super().__init__(name, mode)

        if mode == 'DAU':
            self.solver = DAUSolver()
        elif mode == 'SA':
            self.solver = SASolver()

        self.form.runbutton.clicked.connect(self.runTrigger)
        self.solver.error.connect(self.errorHandlerSlot)

        self.solver.finished.connect(self.finishRunningSlot)

        print(type(self.solver.logger.log_signal))
        self.solver.logger.log_signal.connect(self.log.append)

    def runTrigger(self):
        parameters = self.form.parameters()
        print(parameters)
        self.solver.setParameters(**parameters)
        self.solver.start()

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

    def finishRunningSlot(
            self,
            shift: pd.DataFrame,
            algorithm_data: pd.DataFrame):
        # print("finishRunningSlot")
        # print(id(self.table))
        self.table.loadDataFrame(shift)
        self.algorithm_table.loadDataFrame(algorithm_data)
        self.form.runbutton.setDisabled(False)


if __name__ == "__main__":
    os.mkdir('jobs')

    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver)  # pass type
    win.show()
    sys.exit(app.exec())
