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
    finished = Signal(pd.DataFrame)
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

        def generateShiftFromTable(table, namelist):
            """
            This function generates a pandas dataframe from a table which is a 2-D array.
            The first row of the dataframe is name, 1, 2, ..., n days
            The first column of the dataframe is the name of the workers

            Args:
                table: a 2-D array
                namelist: a list of names of the workers
            
            Returns:
                a pandas dataframe
            """
            df = pd.DataFrame(table, columns=[str(i) for i in range(1, len(table[0]) + 1)])
            df.insert(0, "name", namelist)
            return df
        
        def generateShifts(tables, namelist):
            dataframes = []
            for i in range(len(tables)):
                dataframes.append(generateShiftFromTable(tables[i], namelist))

            return dataframes
        try:
            self.compile()
            self.tables = self.solve()
            self.shifts = generateShifts(self.tables, self._namelist)
        except Exception as e:
            self.error.emit(str(e))
            return
        print(self.solutions)
        self.finished.emit(self.shifts[0])


if __name__ == '__main__':

    test_solver = TestSolver()
    shift = test_solver.getShift(0)
    print(shift)