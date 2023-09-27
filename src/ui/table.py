import sys
from ui.table_widget import TableWidgetItem
from PySide6.QtWidgets import QTableWidget, QApplication



if __name__ == '__main__':
    app = QApplication([])

    table = QTableWidget()

    table.setRowCount(10)
    table.setColumnCount(10)

    for i in range(10):
        for j in range(10):
            item = TableWidgetItem()
            item.setText(str(i + j))
            table.setItem(i, j, item)

    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.show()

    sys.exit(app.exec())