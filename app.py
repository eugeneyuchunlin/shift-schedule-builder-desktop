import sys
from PySide6.QtWidgets import QApplication
from src.ui.ui import MainWindow
import os


if __name__ == "__main__":

    if not os.path.exists('jobs'):
        os.mkdir('jobs')

    app = QApplication(sys.argv)
    win = MainWindow()  # pass type
    win.show()
    sys.exit(app.exec())
