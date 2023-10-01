from PySide6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout)
from src.model.user import User
from src.model.data_adapter import DataAdapter

from .working_area import WorkingArea



class Tabs(QWidget):
    """
    This class is used to create a tab widget and handle tabs.

    The tab widget contains the following components:
        - a tab widget
        - a list of tabs
        - a list of names of the tabs

    The tab widget is a subclass of QWidget class and it provides the following methods:
        - initUI: create the tab widget
        - addANewTab: add a new tab to the tab widget
        - createATab: create a new tab
        - switchToLastTab: switch to the last tab
        - exportWorkingArea: export the working area to a three dataframes
        - currentTab: get the current tab
        - setCurrentTabName: set the name of the current tab

    Attributes:
        configuration_type: the type of the tab
        number_of_untitled_tabs: the number of untitled tabs
        tabwidget: the tab widget
        tabs: the list of tabs
        names: the list of names of the tabs
    """

    tabs = []
    names = []

    def __init__(self, user:User):
        """
        This is the constructor of the Tabs class. It calls the constructor of the QWidget class.
        You can specify the type of the tab by setting the configurationType argument.

        """
        super().__init__()
        self.user = user
        self.number_of_untitled_tabs = 0  # FIXME: deprecated

        # self.initUI()

        self.tabwidget = QTabWidget()
        shift_ids = user.getShifts()
        if len(shift_ids) == 0:
            self.addANewTab()
        else:
            for shift_id in shift_ids:
                self.addANewTab(shift_id)
        vbox = QVBoxLayout()
        vbox.addWidget(self.tabwidget)
        self.setLayout(vbox)

    # def initUI(self):
    #     """
    #     This method initializes the ui and creates a tab widget.
    #     """
    #     self.tabwidget = QTabWidget()

    #     # self.addANewTab()

    #     vbox = QVBoxLayout()
    #     vbox.addWidget(self.tabwidget)

    #     self.setLayout(vbox)

    def addANewTab(self, shift_id=None):
        """
        This method adds a new tab to the tab widget.
        """

        self.number_of_untitled_tabs += 1
        new_tab = self.createATab(
            "Untitiled" + str(self.number_of_untitled_tabs), shift_id)
        self.tabs.append(new_tab)
        self.tabwidget.addTab(new_tab, new_tab.name)

    def createATab(self, name: str, shift_id=None) -> QWidget:
        """
        This method creates a new tab.
        """
        tab = WorkingArea(name, self.user, shift_id)
        return tab

    def switchToLastTab(self):
        """
        This method switches to the last tab.
        """
        self.tabwidget.setCurrentIndex(self.number_of_untitled_tabs - 1)

    def exportWorkingArea(self) -> tuple:
        """
        This method exports the working area to a three dataframes.

        Returns:
            A tuple of three dataframes: the shift table, the algorithm table, and the form.
        """
        working_area = self.tabs[self.tabwidget.currentIndex()]
        return working_area.table.exportTableToDataFrame()

    def currentTab(self) -> QWidget:
        """
        This method gets the current tab.

        Returns:
            The current tab in QWidget type.
        """
        return self.tabs[self.tabwidget.currentIndex()]

    def setCurrentTabName(self, new_name: str):
        """
        This method sets the name of the current tab.

        Args:
            new_name: the new name of the current tab
        """
        self.tabwidget.setTabText(self.tabwidget.currentIndex(), new_name)

