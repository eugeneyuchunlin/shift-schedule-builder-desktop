import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets
from src.ui.ui import MainWindow
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":

    if not os.path.exists('jobs'):
        os.mkdir('jobs')

    app = QApplication(sys.argv)
    # view = QtWebEngineWidgets.QWebEngineView()
    # filename = os.path.join(CURRENT_DIR, 'views/login.html')
    # print(filename)
    # view.load(QtCore.QUrl.fromLocalFile(filename))
    # view.show()
    win = MainWindow()  # pass type
    win.show()
    sys.exit(app.exec())
