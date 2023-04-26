import sys
from PySide6.QtWidgets import QApplication
from ui import MainWindow, WorkingArea
from NSP_test_230413 import Solver

import pandas as pd
import threading


class NSPSolver(WorkingArea, Solver):

    def __init__(self, name):
        super().__init__(name)
        super(Solver, self).__init__()

        self.form.runbutton.clicked.connect(self.runTrigger)

    def solve(
            self,
            per_grave,
            n1,
            k,
            num_sweeps,
            year,
            month,
            lmda,
            lmdb,
            lmdc,
            lmdd,
            lmde):

        shift, dataframe = super().solve(per_grave, n1, k, num_sweeps,
                                         year, month, lmda, lmdb, lmdc, lmdd, lmde)
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

        self.running_thread = threading.Thread(
            target=self.solve,
            args=[
                per_grave,
                n1,
                k,
                num_sweeps,
                year,
                month,
                lmda,
                lmdb,
                lmdc,
                lmdd,
                lmde])
        self.running_thread.daemon = True
        self.running_thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver)  # pass type
    win.show()
    sys.exit(app.exec())
