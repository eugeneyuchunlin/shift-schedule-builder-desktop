import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Signal
from ui import MainWindow, WorkingArea
from NSP_test_230413 import Solver

import pandas as pd
import threading


class NSPSolver(WorkingArea, Solver):

    error = Signal(str)

    def __init__(self, name, form_config):
        super().__init__(name, form_config)
        super(Solver, self).__init__()

        self.form.runbutton.clicked.connect(self.runTrigger)
        self.error.connect(self.showAlertMessageBox)

    def getBasicParameters(self):
        pass

    def solveDAU(self):
        parameters = self.form.parameters()
        per_grave = int(parameters["per_grave"])
        per_num = int(parameters["per_num"])
        per_night = int(parameters["per_night"])
        n1 = int(parameters["n1"])
        n2 = int(parameters["n2"])
        n = int(parameters["n"])
        k = int(parameters["k"])
        num_sweeps = int(parameters["num_sweeps"])
        year = int(parameters["year"])
        month = int(parameters["month"])
        lmda = float(parameters["lmda"])
        lmdb = float(parameters["lmdb"])
        lmdc = float(parameters["lmdc"])
        lmdd = float(parameters["lmdd"])
        lmde = float(parameters["lmde"])
        time_limit = int(parameters["time_limit_sec"])
        penalty_coef = int(parameters["penalty_coef"])

        print("Solve by employing the DAU")

        try:
            shift, algorithm_data = super().solveDAU(per_grave, per_num, per_night, n1, n2, n,
                                                     k, num_sweeps, year, month, lmda, lmdb, lmdc, lmdd, lmde, time_limit, penalty_coef)
        except Exception as e:
            # Show the error message
            self.error.emit(str(e))
            return
        print(shift)
        self.table.loadDataFrame(shift)
        self.algorithm_table.loadDataFrame(algorithm_data)
        self.running_thread = None

    def solveSA(self):
        parameters = self.form.parameters()
        per_grave = int(parameters["per_grave"])
        n1 = int(parameters["n1"])
        k = int(parameters["k"])
        num_sweeps = int(parameters["num_sweeps"])
        year = int(parameters["year"])
        month = int(parameters["month"])
        lmda = float(parameters["lmda"])
        lmdb = float(parameters["lmdb"])
        lmdc = float(parameters["lmdc"])
        lmdd = float(parameters["lmdd"])
        lmde = float(parameters["lmde"])
        try:
            shift, dataframe = super().solveSA(per_grave, n1, k, num_sweeps,
                                               year, month, lmda, lmdb, lmdc, lmdd, lmde)
        except Exception as e:
            self.error.emit(str(e))
            return
        # dataframe = pd.read_csv("./Graveyard_shift.csv")
        # shift = []
        # for i in range(10):
        #     shift.append([i for i in range(31)])
        # shift = pd.DataFrame(shift, columns=[str(i) for i in range(31)])

        self.table.loadDataFrame(shift)
        self.algorithm_table.loadDataFrame(dataframe)
        self.running_thread = None

    def runTrigger(self):
        # collect the parameters
        # TODO: I should check the type and the data format for each parameter
        DAUorSA = self.form.runningMode()
        print(DAUorSA)
        if DAUorSA == 'DAU':
            self.running_thread = threading.Thread(target=self.solveDAU)
        else:
            self.running_thread = threading.Thread(target=self.solveSA)

        self.running_thread.daemon = True
        self.running_thread.start()

    def showAlertMessageBox(self, alert_msg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(alert_msg)
        msg.setWindowTitle("Error")
        msg.addButton(QMessageBox.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver)  # pass type
    win.show()
    sys.exit(app.exec())
