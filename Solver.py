from PySide6.QtCore import Signal, QThread
from DAUSolver import QuantumAnnealingAlgorithm
from SASolver import SimulatedAnnealingAlgorithm

import pandas as pd

class Solver(QThread):

    progress = Signal(int)
    finished = Signal(pd.DataFrame, pd.DataFrame)
    error = Signal(str)

    def __init__(self):

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
        try:
            shift, algorithm_data = self.solve(**self._parameters)
        except Exception as e:
            self.error.emit(str(e))
            return
        self.finished.emit(shift, algorithm_data)



class SASolver(Solver, SimulatedAnnealingAlgorithm):

    def __init__(self):
        super().__init__()
        super(SimulatedAnnealingAlgorithm, self).__init__()

    def run(self):
        try:
            shift, algorithm_data = self.solve(**self._parameters)
        except Exception as e:
            self.error.emit(str(e))
            return
        self.finished.emit(shift, algorithm_data)