from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QLabel,
    QPushButton, QVBoxLayout, QMessageBox
)

from src.model.data_adapter import DataAdapter

class LoginDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setModal(True)

        self.layout = QVBoxLayout()
        formlayout = QFormLayout()
        self._username_label = QLabel("Username")
        self._username_edit = QLineEdit()
        formlayout.addRow(self._username_label, self._username_edit)

        self._password_label = QLabel("Password")
        self._password_edit = QLineEdit()
        formlayout.addRow(self._password_label, self._password_edit)

        self._login_btn = QPushButton("Login")
        self.layout.addWidget(self._login_btn)
        self._login_btn.clicked.connect(self.login)

        self.layout.addLayout(formlayout)
        self.setLayout(self.layout)

    def login(self):
        self._username = self._username_edit.text()
        self._password = self._password_edit.text()

        print(self._username, self._password)

        # check if the username and password are correct
        if(self._username == "" or self._password == ""):
            self.UserNotExist()
            return 
        else:
            self.user = DataAdapter().getUser(self._username, self._password)
            if self.user is None:
                self.UserNotExist()
                return 
            else:
                self.close()
                return

    def getLoginInfo(self):
        return {
            "username": self._username,
            "password": self._password
        }

    def getUser(self):
        return self.user
    
    def UserNotExist(self):
        usernotexist=QMessageBox()
        usernotexist.setWindowTitle("Warning")
        usernotexist.setText("The user does not exist!")
        usernotexist.setButtonText(1,"Close")
        usernotexist.exec()