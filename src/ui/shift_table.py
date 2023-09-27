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

    def createShiftTable(self, number_of_people: int, year: int, month: int):
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
        days = calendar.monthrange(year, month)[1]

        self.setRowCount(number_of_people)
        self.setColumnCount(days)
        self.setHorizontalHeaderLabels([str(i) for i in range(1, days + 1)])
        self.setVerticalHeaderLabels(
            [str(i) for i in range(1, number_of_people + 1)])

        self.resizeColumnsToContents()