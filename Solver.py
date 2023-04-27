from PySide6.QtCore import Signal, QThread
from DAUSolver import QuantumAnnealingAlgorithm
from SASolver import SimulatedAnnealingAlgorithm

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

    def setParameters(self, **kwargs):
        self._parameters = kwargs
        pass


class DAUSolver(Solver, QuantumAnnealingAlgorithm):

    def __init__(self):
        super().__init__()
        super(QuantumAnnealingAlgorithm, self).__init__()
        pass

    def run(self):
        # print("DAUSolver run")
        try:
            self.shift, self.algorithm_data = self.solve(**self._parameters)
        except Exception as e:
            self.error.emit(str(e))
            return
        self.finished.emit(self.shift, self.algorithm_data)



class SASolver(Solver, SimulatedAnnealingAlgorithm):

    def __init__(self):
        super().__init__()
        super(SimulatedAnnealingAlgorithm, self).__init__()

    def run(self):
        # print("SASolver run")
        try:
            self.shift, self.algorithm_data = self.solve(**self._parameters)
        except Exception as e:
            self.error.emit(str(e))
            return
        self.finished.emit(self.shift, self.algorithm_data)