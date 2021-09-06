import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pyodbc
from error import *
from PyQt5 import QtGui
from PyQt5.QtCore import QDate

class NotePopUp(QDialog):
    def __init__(self, SID, database, notes):
        super(NotePopUp, self).__init__()
        loadUi("ui/mttNotePopUp.ui", self)
        self.courses_ID = {}
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.SID = SID
        self.conn = pyodbc.connect(database)
        self.notes = notes
    
    def fillCombo(self, courseID=-111):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Courses WHERE SID=" + str(self.SID))
        for row in cursor:
            if not courseID == row[1]:
                self.comboBox.addItem(row[1])
                self.courses_ID[row[1]] = row[0]

    
    def addNote(self):
        if(len(self.textEdit.toPlainText()) == 0):
            self.error = Error("You left some fields empty")
            self.error.show()
            return
        course = str(self.comboBox.currentText())
        currentDate = QDate.currentDate().toString('yyyy-MM-dd')
        content = self.textEdit.toPlainText()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Notes(courseID, Date, Content, SID, Course_Id ) \
        VALUES('%s', '%s', '%s', '%s',%s)" %(course, currentDate, content, self.SID, self.courses_ID[course]))
        self.notes.append([course, currentDate, content, self.SID])
        cursor.commit()
        self.close()

