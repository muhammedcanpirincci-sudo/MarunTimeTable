import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from error import *
import pyodbc


class ChangePassword(QDialog):
    def __init__(self, SID, database):
        super(ChangePassword, self).__init__()
        loadUi("ui/mttChangePassword.ui", self)
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.changeButton.clicked.connect(self.change)

        self.sid = SID
        self.conn = pyodbc.connect(database)

    def change(self):
            cursor = self.conn.cursor()
            password = self.lineEdit.text()
            if len(password) == 0:
                self.errorWindow = Error("You left field/s empty")
                self.errorWindow.show()
                return
            cursor.execute("UPDATE Student SET Password='%s' WHERE SID='%s'" % (password, str(self.sid)))
            cursor.commit()
            self.close()
