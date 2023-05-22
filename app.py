import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ui import MainWindow, WorkingArea

from DAUSolver import QuantumAnnealingAlgorithm
from SASolver import SimulatedAnnealingAlgorithm

import pandas as pd
import os


class NSPSolver(WorkingArea):

    # TODO: enable user to register new solver
    def __init__(self, name, mode):
        super().__init__(name, mode)

        if mode == 'DAU':
            self.solver = QuantumAnnealingAlgorithm()
        elif mode == 'SA':
            self.solver = SimulatedAnnealingAlgorithm()
    
        # Connect the signals and slots, especially for triggers
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

        # Enable user to select solution
        self.form.index_of_solution_edit.editingFinished.connect(self.indexOfSolutionTrigger)


    def indexOfSolutionTrigger(self):
        index = int(self.form.index_of_solution_edit.text())
        self.table.loadDataFrame(self.solver.transformSolutionToTable(index))


if __name__ == "__main__":

    if not os.path.exists('jobs'):
        os.mkdir('jobs')

    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver)  # pass type
    win.show()
    sys.exit(app.exec())
