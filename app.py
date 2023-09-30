import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from src.ui.ui import MainWindow
from src.ui.working_area import WorkingArea
from src.model.data_adapter import DataAdapter
from src.algorithms.Solvers import DAUSolver, SASolver, MockSolver
from src.model.user import User
import pandas as pd
import os


if __name__ == "__main__":

    if not os.path.exists('jobs'):
        os.mkdir('jobs')

    app = QApplication(sys.argv)
    win = MainWindow()  # pass type
    win.show()
    sys.exit(app.exec())
