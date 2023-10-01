from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from .table_widget import TableWidget
import calendar

class ShiftTable(TableWidget):
    """
    This class is used to create a shift table.

    ShiftTable is a subclass of TableWidget class and it provides the following methods:
        - createShiftTable: create an empty shift table
    """

    # TODO: remove the empty_table argument
    def __init__(
            self,
            empty_table=True,
            number_of_rows=None,
            year=None,
            month=None):
        """
        This is the constructor of the ShiftTable class. It calls the constructor of the TableWidget class.
        You can specify whether the class should create an empty table or not by setting the empty_table argument.
        The number of days of the shift table depends on the year and month arguments.

        Args:
            empty_table: a boolean value to indicate whether the class should create an empty
                table or not. The default value is True.
            number_of_rows: the number of rows of the table
            year: the year of this shift table
            month: the month of this shift table
        """
        super().__init__()

    def createShiftTable(self, number_of_people: int, **kwargs):
        """
        This method creates an empty shift table

        You can use this method to create an empty shift table. The number of days of the shift table depends on the year and month arguments.
        The number of rows of the shift table depends on the number_of_people argument.

        Args:
            number_of_people: the number of people
            year: the year of this shift table
            month: the month of this shift table
        """
        # FIXME handle the exception of monthrange
        if('days' not in kwargs) and ('year' not in kwargs or 'month' not in kwargs):
            raise Exception('you have to give either days or year and month to the function')
        
        if('days' in kwargs):
            days = kwargs['days']
        else:
            days = calendar.monthrange(kwargs['year'], kwargs['month'])[1]

        self.setRowCount(number_of_people)
        self.setColumnCount(1 + days)

        self.setHorizontalHeaderLabels(['name'] + [str(i) for i in range(1, days + 1)])
        self.setVerticalHeaderLabels(
            [str(i) for i in range(1, number_of_people + 1)])

        # set name
        for i in range(number_of_people):
            item = QTableWidgetItem('name' + str(i + 1))
            self.setItem(i, 0, item)
        
        # initialize content of the table, set to 1
        for i in range(number_of_people):
            for j in range(1, days + 1):
                item = QTableWidgetItem('1')
                self.setItem(i, j, item)


        self.resizeColumnsToContents()

    def getContent(self):
        """
        This method returns the content of the table as a list.
        The structure of the list is as follows:
            [
                {
                    "name": "name1",
                    "shift_array" : []
                }

            ]        

        Returns:
            A list
        """

        content = []
        for i in range(self.rowCount()):
            row = {}
            row['name'] = self.item(i, 0).text()
            row['shift_array'] = []
            for j in range(1, self.columnCount()):
                row['shift_array'].append(self.item(i, j).text())
            content.append(row)
        return content
    
    def getNameList(self):
        """
        This method returns the name list of the table as a list.

        Returns:
            A list
        """
        name_list = []
        for i in range(self.rowCount()):
            name_list.append(self.item(i, 0).text())
        return name_list