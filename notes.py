import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime, Qt, QDate
from PyQt5.QtGui import QPixmap
from settings import *
from notePopUp import *
from datetime import datetime


class Notes(QDialog):
    def __init__(self, widget, loginWidget, window_indexes, database, SID, settingsWindow):
        super(Notes, self).__init__()
        loadUi("ui/mttNotes.ui", self)
        self.widget = widget
        self.loginWidget = loginWidget
        self.courses = []
        self.notes = []
        self.window_indexes = window_indexes
        self.goBackButton.clicked.connect(lambda:self.widget.setCurrentIndex(self.window_indexes["dashboard"]))
        self.coursesButton.clicked.connect(lambda:self.widget.setCurrentIndex(self.window_indexes["courses"]))
        self.eventsButton.clicked.connect(lambda:self.widget.setCurrentIndex(self.window_indexes["events"]))
        self.logoutButton.clicked.connect(self.logout)
        self.addNotePopUp = NotePopUp(SID, database, self.notes)
        self.addNoteButton.clicked.connect(self.add_note)
        self.conn = pyodbc.connect(database)
        self.database = database
        self.SID=SID
        self.fullname = ''
        self.email = ''
        self.preNotesLen = 0
        self.settingButton.clicked.connect(self.goto_settings)
        self.add_user_info()
        self.get_notes()
        self.add_notes_GUI()
        self.settingsWindow = settingsWindow
        timer = QTimer(self)
        timer.timeout.connect(self.add_time_date)
        timer.start(100)
    
    def add_note(self):
        self.addNotePopUp.fillCombo()
        self.addNotePopUp.pushButton.clicked.connect(self.addNotePopUp.addNote)
        self.addNotePopUp.show()

    def get_notes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Notes WHERE SID=%s" % str(self.SID))
        for row in cursor:
            self.notes.append([row[1], row[2], row[3], row[4], row[0]])
        self.preNotesLen = len(self.notes)

    def add_notes_GUI(self):
        for note in self.notes:
            button = QPushButton()
            button.setObjectName(note[0])
            button.clicked.connect(self.edit_note)
            d = note[1]
            date_str = d.strftime('%Y-%m-%d')
            button.setText(note[0] + " " + date_str)
            self.formLayout.addRow(button)
    
    def edit_note(self):
        courseID = self.sender().objectName()
        noteID = ""
        self.window = NotePopUp(self.SID, self.database, self.notes)
        self.add_delete_button(self.window)
        for note in self.notes:
            if note[0] == courseID:
                self.window.textEdit.setText(note[2])
                noteID = note[4]
                break
        self.window.comboBox.addItem(courseID)
        self.window.pushButton.setText("Apply")
        self.window.pushButton.clicked.connect(lambda:self.update_note(noteID))
        self.window.show()
    
    def update_note(self, noteID):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE Notes \
            SET content='%s' \
            WHERE NoteID='%s'" %
            (self.window.textEdit.toPlainText(), noteID))
        cursor.commit()
        self.window.close()
        for note in self.notes:
            if note[4] == noteID:
                note[2] = self.window.textEdit.toPlainText()

    def logout(self):
        self.widget.close()
        self.loginWidget.setCurrentIndex(0)
        self.loginWidget.show()

    def add_user_info(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Student WHERE SID=%s" % str(self.SID))
        for row in cursor:
            self.email = row[3]
            self.fullname = row[1].capitalize() + " " + row[2].capitalize()
            self.nameSurname.setText(self.fullname)
            break

    def add_time_date(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()
        self.date.setText(currentDate.toString())
        self.time.setText(currentTime.toString('hh:mm:ss'))
        pix = QPixmap("profile.png")
        self.picture.setPixmap(pix)
        self.fullname = self.settingsWindow.fullname
        self.nameSurname.setText(self.fullname)
        self.notes = self.addNotePopUp.notes
        if self.preNotesLen != len(self.notes):
            self.preNotesLen = len(self.notes)
            button = QPushButton()
            button.setObjectName(self.notes[len(self.notes)-1][0])
            button.clicked.connect(self.edit_note)
            button.setText(self.notes[len(self.notes)-1][0] + " " + self.notes[len(self.notes)-1][1])
            self.formLayout.addRow(button)

    def goto_settings(self):
        self.settingsWindow.show()
        self.settingsWindow.setWindowTitle("Settings")       
