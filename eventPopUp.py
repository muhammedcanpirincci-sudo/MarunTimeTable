import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pyodbc
from error import *
from PyQt5 import QtGui
from PyQt5.QtCore import QDate

class EventPopUp(QDialog):
    def __init__(self, database, SID, events):
        super(EventPopUp, self).__init__()
        loadUi("ui/mttEventPopUp.ui", self)
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.conn = pyodbc.connect(database)
        self.SID = SID
        self.events = events
    
    def addEvent(self):
        if(len(self.lineEdit.text()) == 0 or len(self.textEdit.toPlainText()) == 0):
            self.error = Error("You left some fields empty")
            self.error.show()
            return
        date = self.dateEdit.date().toString('yyyy-MM-dd')
        title = self.lineEdit.text()
        currentDate = QDate.currentDate().toString('yyyy-MM-dd')
        content = self.textEdit.toPlainText()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO EVENT(start_date, end_date, Name, Description, SID) \
        VALUES('%s', '%s', '%s', '%s','%s')" %(currentDate, date, title, content, self.SID))
        self.events.append([currentDate, date, title, content, self.SID])
        cursor.commit()
        self.close()

        
