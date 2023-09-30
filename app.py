import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from src.ui.ui import MainWindow
from src.ui.working_area import WorkingArea
from src.model.data_adapter import DataAdapter
from src.algorithms.Solvers import DAUSolver, SASolver, MockSolver
from src.model.user import User
import pandas as pd
import os


class NSPSolver(WorkingArea):

    # TODO: enable user to register new solver
    def __init__(self, name, user:User):
        super().__init__(name, user)

        # if mode == 'DAU':
        #     self.solver = QuantumAnnealingAlgorithm()
        # elif mode == 'SA':
        #     self.solver = SimulatedAnnealingAlgorithm()
        # Connect the signals and slots, especially for triggers
        self.form.runbutton.clicked.connect(self.runTrigger)

    def runTrigger(self):
        content = self.table.getContent()
        print(content)
        self.parameters = self.form.parameters()
        self.parameters['content'] = content

        if self.parameters['type'] == 'DAU':
            self.solver = MockSolver(problem=self.parameters)
        elif self.parameters['type'] == 'SA':
            self.solver = MockSolver(problem=self.parameters)
            
        self.solver.error.connect(self.errorHandlerSlot)
        self.solver.finished.connect(self.finishRunningSlot)

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
            shift: pd.DataFrame):
        # print("finishRunningSlot")
        # print(id(self.table))
        self.table.loadDataFrame(shift)
        data = {
            "shift_id": self.shift_id,
            "parameters" : self.parameters,
            "shift": shift
        }
        print(self.user.getUsername())
        DataAdapter().saveShift(self.user, data)
        self.form.runbutton.setDisabled(False)



if __name__ == "__main__":

    if not os.path.exists('jobs'):
        os.mkdir('jobs')

    app = QApplication(sys.argv)
    win = MainWindow(NSPSolver)  # pass type
    win.show()
    sys.exit(app.exec())
