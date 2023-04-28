from PySide6.QtCore import Signal, QThread
from console import Logger
import pandas as pd


class Solver(QThread):

    progress = Signal(int)
    finished = Signal(pd.DataFrame, pd.DataFrame)
    error = Signal(str)

    def __init__(self):
        # self.shift = []
        # for i in range(10):
        #     self.shift.append([0] * 31)

        # self.shift = pd.DataFrame(self.shift, columns=[str(i) for i in range(1, 32)])

        # self.algorithm_data = []
        # self.algorithm_data = pd.read_csv('.\Graveyard_shift.csv')

        super().__init__()
        self.logger = Logger()

    def setParameters(self, **kwargs):
        self._parameters = kwargs
        pass

    def solver(self):
        pass

    def run(self):
        try:
            self.shift, self.algorithm_data = self.solve(**self._parameters)
        except Exception as e:
            self.error.emit(str(e))
            return
        self.finished.emit(self.shift, self.algorithm_data)
        pass
