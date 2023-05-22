from PySide6.QtCore import Signal, QThread
from console import Logger
import pandas as pd
import numpy as np

import calendar

class Solver(QThread):

    progress = Signal(int)
    finished = Signal(pd.DataFrame, pd.DataFrame)
    error = Signal(str)

    solutions = []
    algorithm_data = None

    def __init__(self):

        super().__init__()
        self.logger = Logger()

    def setParameters(self, **kwargs):
        self._parameters = kwargs
        pass

    def solver(self):
        pass

    def generateShiftFromSolution(self, per_grave, days, solution_dict):
        table = np.zeros(per_grave * days)
        for key, value in solution_dict.items():
            if "Graveyard" in key and "*" not in key:
                newkey = int(key.replace("Graveyard[", "").replace("]", ""))
                table[newkey] = value
        table = table.reshape(per_grave, days).astype(int)
        return table


    def transformSolutionToTable(self, index):
        solution = self.solutions[index]
        firstday, days = calendar.monthrange(int(self._parameters["year"]), int(self._parameters["month"]))
        table = self.generateShiftFromSolution(int(self._parameters['per_grave']), days, solution)

        table_df = pd.DataFrame(table, columns=[str(i) for i in range(1, days + 1)])
        return table_df

    def run(self):
        try:
            self.solutions, self.algorithm_data = self.solve(**self._parameters)
            self.shift = self.transformSolutionToTable(int(self._parameters["index_of_solution"])) 
        except Exception as e:
            self.error.emit(str(e))
            return
        # print(self.solutions)
        self.finished.emit(self.shift, self.algorithm_data)
