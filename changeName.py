import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pyodbc
from error import *
from PyQt5 import QtGui

class ChangeName(QDialog):
    def __init__(self, SID, database, fullname):
        super(ChangeName, self).__init__()
        loadUi("ui/mttChangeName.ui", self)
        self.changeButton.clicked.connect(self.change)
        self.sid = SID
        self.conn = pyodbc.connect(database)
        self.fullname = fullname
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))


    
    def change(self):
        cursor = self.conn.cursor()
        first_name = self.lineEdit.text()
        surname = self.lineEdit_2.text()
        if len(first_name)==0 or len(surname)==0:
            self.errorWindow = Error("You left field/s empty")
            self.errorWindow.show()
            return
        self.fullname = first_name + " " + surname
        cursor.execute("UPDATE Student SET Name='%s', Surname='%s' WHERE SID='%s'" % (first_name, surname, str(self.sid)))
        cursor.commit()
        self.close()



