from PySide6.QtCore import Signal, QThread
from .console import Logger
import pandas as pd
import numpy as np


class TestSolver(object):

    __shifts = []
    def __init__(self):
        super().__init__()

        # load solutions

        shift_df = pd.read_excel("test.xlsx", sheet_name="shift", index_col=0)
        self.__parameter_df = pd.read_excel("test.xlsx", sheet_name="parameters", index_col=0)

        self.__shifts.append(shift_df)

    def getShift(self, i):
        return self.__shifts[i]
    
    def getParameters(self, i):
        return self.__parameter_df

class Solver(QThread):

    progress = Signal(int)
    finished = Signal(list)
    error = Signal(str)

    solutions = []
    shifts = []
    algorithm_data = None

    def __init__(self):

        super().__init__()
        self.logger = Logger()

    def setParameters(self, **kwargs):
        self._parameters = kwargs
        pass

    def run(self):
        try:
            self.compile()
            self.tables = self.solve()
        except Exception as e:
            self.error.emit(str(e))
            return
        self.finished.emit(self.tables)


if __name__ == '__main__':

    test_solver = TestSolver()
    shift = test_solver.getShift(0)
    print(shift)