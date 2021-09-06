import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pyodbc

class Register(QDialog):

    def __init__(self, widget, window_indexes, database):
        super(Register, self).__init__()
        self.conn = pyodbc.connect(database)
        self.widget = widget
        self.window_indexes = window_indexes
        loadUi("ui/mttRegister.ui", self)
        self.goBackButton.clicked.connect(self.goto_login)
        self.registerButton.clicked.connect(self.create_account)


    def goto_login(self):
        self.widget.setCurrentIndex(self.window_indexes["login"])

    def reset_register(self):
        self.errorLabel.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

    def create_account(self):
        # TODO Error Checking like (all lineedits are full, no repeated sid or email)
        sid = self.lineEdit_5.text()
        name = self.lineEdit_3.text()
        surname = self.lineEdit_4.text()
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        cursor = self.conn.cursor()

        if len(sid) == 0 or len(name) == 0 or len(surname) == 0 or len(email) == 0 or len(password) == 0:
            self.errorLabel.setText("You left one or more fields empty")
            return
        try:
            cursor.execute(
                "INSERT INTO Student(SID,Name,Surname,Email,Password) values(?,?,?,?,?)",
                (sid, name, surname, email, password)
            )
            self.conn.commit()
            print("in create account")
            cursor.execute("SELECT * FROM Student")
            for row in cursor:
                print(f'row = ', row[3], row[4])
            self.goto_login()
            self.reset_register()
        except:
            self.errorLabel.setText("User already exists")
    