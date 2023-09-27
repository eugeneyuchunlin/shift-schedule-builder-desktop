from PySide6.QtCore import Signal, QThread
from .console import Logger
import pandas as pd
import numpy as np

import calendar

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
    finished = Signal(pd.DataFrame, pd.DataFrame)
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

        def generateShiftFromSolution(per_grave, days, solution_dict):
            table = np.zeros(per_grave * days)
            for key, value in solution_dict.items():
                if "Graveyard" in key and "*" not in key:
                    newkey = int(key.replace("Graveyard[", "").replace("]", ""))
                    table[newkey] = value
            table = table.reshape(per_grave, days).astype(int)
            return table
        
        def transformSolutionToTable(solution):
            firstday, days = calendar.monthrange(int(self._parameters["year"]), int(self._parameters["month"]))
            table = generateShiftFromSolution(int(self._parameters['per_grave']), days, solution)

            table_df = pd.DataFrame(table, columns=[str(i) for i in range(1, days + 1)])
            return table_df

        try:
            self.solutions, self.algorithm_data = self.solve(**self._parameters)
            self.shifts = []
            for i in range(len(self.solutions)):
                self.shifts.append(transformSolutionToTable(self.solutions[i]))
        except Exception as e:
            self.error.emit(str(e))
            return
        # print(self.solutions)
        self.finished.emit(self.shift, self.algorithm_data)


if __name__ == '__main__':

    test_solver = TestSolver()
    shift = test_solver.getShift(0)
    print(shift)