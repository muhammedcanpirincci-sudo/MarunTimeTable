import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime, Qt, QDate
from PyQt5.QtGui import QPixmap
from settings import *
from eventPopUp import *

class Events(QDialog):
    def __init__(self, widget, loginWidget, window_indexes, database , SID, settingsWindow, events, dashboard):
        super(Events, self).__init__()
        loadUi("ui/mttEvents.ui", self)
        self.widget = widget
        self.loginWidget = loginWidget
        self.window_indexes = window_indexes
        self.goBackButton.clicked.connect(lambda:self.widget.setCurrentIndex(self.window_indexes["dashboard"]))
        self.coursesButton.clicked.connect(lambda:self.widget.setCurrentIndex(self.window_indexes["courses"]))
        self.notesButton.clicked.connect(lambda:self.widget.setCurrentIndex(self.window_indexes["notes"]))
        self.logoutButton.clicked.connect(self.logout)
        self.events = events
        self.addEventPopUp = EventPopUp(database, SID, self.events)
        self.addEventPopUp.pushButton.clicked.connect(self.addEventPopUp.addEvent)
        self.addEventButton.clicked.connect(lambda:self.addEventPopUp.show())
        self.conn = pyodbc.connect(database)
        self.database = database
        self.SID=SID
        self.fullname = ''
        self.email = ''
        self.settingButton.clicked.connect(self.goto_settings)
        self.add_user_info()
        self.settingsWindow = settingsWindow
        self.preEventsLen = len(events)
        self.dashboard = dashboard
        self.add_events_GUI()
        self.refresh = False
        timer = QTimer(self)
        timer.timeout.connect(self.add_time_date)
        timer.start(100)


    def logout(self):
        self.widget.close()
        self.loginWidget.setCurrentIndex(0)
        self.loginWidget.show()
    
    
    def add_events_GUI(self):
        for event in self.events:
            button = QPushButton()
            button.setObjectName(str(event[5]))
            button.clicked.connect(self.edit_event)
            button.setText(event[2])
            self.formLayout.addRow(button)

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
        self.events = self.addEventPopUp.events
        if self.preEventsLen != len(self.events):
            self.preEventsLen = len(self.events)
            button = QPushButton()
            button.clicked.connect(self.edit_event)
            button.setObjectName(str(self.events[len(self.events)-1][4]))
            button.clicked.connect(self.edit_event)
            button.setText(self.events[len(self.events)-1][2])
            self.formLayout.addRow(button)
        if self.refresh:
            for i in reversed(range(self.formLayout.count())): 
                self.formLayout.itemAt(i).widget().setParent(None)
            self.add_events_GUI()
            self.refresh = False

    def edit_event(self):
        for event in self.events:
            if str(event[len(event)-1]) == self.sender().objectName():
                self.window = EventPopUp(self.database, self.SID, self.events)
                self.window.lineEdit.setText(event[2])
                self.window.textEdit.setText(event[3])
                self.window.show()
                self.window.pushButton.setText("Apply")
                self.window.pushButton.clicked.connect(lambda:self.edit_event_apply(event[len(event)-1], self.sender()))

    def edit_event_apply(self, ID, objectButton):
        cursor = self.conn.cursor()
        for event in self.events:
            if event[len(event)-1] == ID:
                Name = self.window.lineEdit.text()
                Description = self.window.textEdit.toPlainText()
                date = self.window.dateEdit.date().toString('yyyy-MM-dd')
        cursor.execute(
            "UPDATE Event \
            SET end_date='%s', \
                Name='%s', \
                Description='%s'\
            WHERE EventID='%s'" %
            (date, Name, Description, ID))
        cursor.commit()
        self.window.close()
        for event in self.events:
            if event[len(event)-1] == ID:
                event[2] = Name
                event[3] = Description
        self.refresh = True
        self.dashboard.refreshNotes = True
            


    def goto_settings(self):
        self.settingsWindow.show()
        self.settingsWindow.setWindowTitle("Settings")     
