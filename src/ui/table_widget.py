from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QPushButton,
    QTabWidget, QTableWidget, QMenu,
    QVBoxLayout, QLabel, QLineEdit,
    QGridLayout, QFormLayout, QTableWidgetItem,
    QTextEdit, QFileDialog, QDialog, QComboBox
)
from PySide6.QtGui import QColor, QBrush
import pandas as pd


class TableWidget(QTableWidget):
    """
    This class is used to create a table widget

    TableWidget is a subclass of QTableWidget class and it provides the following methods:
        - exportTableToDataFrame: export the table to a pandas dataframe
        - loadDataFrame: load the data from a pandas dataframe to the table
    """

    def __init__(self):
        """
        This is the constructor of the TableWidget class

        It calls the constructor of the QTableWidget class and it takes no arguments
        """
        super().__init__()

    def exportTableToDataFrame(self) -> pd.DataFrame:
        """
        This method exports the table to a pandas dataframe

        You can use this method to export the table to a pandas dataframe

        Returns:
            A pandas dataframe
        """
        horizontal_headers = []

        data = {}
        for i in range(self.columnCount()):
            key = self.horizontalHeaderItem(i).text()
            horizontal_headers.append(key)
            data[key] = []
            for j in range(self.rowCount()):
                data[key].append(self.item(j, i).text())

        return pd.DataFrame(data)

    def loadDataFrame(self, df: pd.DataFrame):
        """
        This method loads the data from a pandas dataframe to the table

        You can use this method to load the data from a pandas dataframe to the table.
        The function will automatically set the number of rows and columns of the table and set the horizontal header labels.

        Args:
            df: a pandas dataframe
        """

        self.setRowCount(df.shape[0])
        self.setColumnCount(df.shape[1])

        self.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i][j]))
                self.setItem(i, j, item)

        self.resizeColumnsToContents()

    