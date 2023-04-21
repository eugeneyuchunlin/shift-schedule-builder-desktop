import sys
from PySide6.QtWidgets import QApplication
from ui import MainWindow, Configuration, ShiftTable
from NSP_test_230413 import Solver

class NSPSolver(Configuration, Solver):

    def __init__(self, table:ShiftTable):
        super().__init__(table)
        super(Solver, self).__init__()

        self.runbutton.clicked.connect(self.runTrigger)

    def runTrigger(self):
        # collect the parameters
        # TODO: I should check the type and data format of each parameter
        print("Run!!!")
        per_grave = int(self.per_grave_edit.text())
        n1 = int(self.n1_edit.text())
        k = int(self.k_edit.text())
        num_sweeps = int(self.num_sweeps_edit.text())
        year = int(self.year_edit.text())
        month = int(self.month_edit.text())
        lmda = float(self.lmda_edit.text())
        lmdb = float(self.lmdb_edit.text())
        lmdc = float(self.lmdc_edit.text())
        lmdd = float(self.lmdd_edit.text())
        lmde = float(self.lmde_edit.text())

        self._solve(per_grave, n1, k, num_sweeps, year, month, lmda, lmdb, lmdc, lmdd, lmde)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver) # pass type
    win.show()
    sys.exit(app.exec())
