import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from error import *
import pyodbc

class ChangeEmail(QDialog):
    def __init__(self, SID, database, email):
        super(ChangeEmail, self).__init__()
        loadUi("ui/mttChangeEmail.ui", self)
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.changeButton.clicked.connect(self.change)
        self.userEmail = email
        self.sid = SID
        self.conn = pyodbc.connect(database)

    def change(self):
            cursor = self.conn.cursor()
            email = self.lineEdit.text()
            if len(email) == 0:
                self.errorWindow = Error("You left field/s empty")
                self.errorWindow.show()
                return
            cursor.execute("UPDATE Student SET Email='%s' WHERE SID='%s'" % (email, str(self.sid)))
            cursor.commit()
            self.userEmail = email
            self.close()

