import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime, Qt, QDate
from courses import *
from coursePopUp import *
from eventPopUp import *
from settings import *
from eventPopUp import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


class Dashboard(QDialog):
    def __init__(self, widget, loginWidget, window_indexes, database, SID, events):
        super(Dashboard, self).__init__()
        loadUi("ui/mttDashboard.ui", self)
        self.widget = widget
        self.courses = []
        self.loginWidget = loginWidget
        self.loginWidget = loginWidget
        self.window_indexes = window_indexes
        self.SID = SID
        self.events = events
        self.usedButtons = {}
        self.fullname = ""
        self.database = database
        self.reset_button_labels()
        self.eventsButton.clicked.connect(lambda:self.go_to("events"))
        self.coursesButton.clicked.connect(lambda:self.go_to("courses"))
        self.notesButton.clicked.connect(lambda:self.go_to("notes"))
        self.addEventPopUp = EventPopUp(database, SID, self.events)
        self.addEventButton.clicked.connect(self.add_event)
        self.settingButton.clicked.connect(self.goto_settings)
        self.logoutButton.clicked.connect(self.logout)
        self.conn = pyodbc.connect(database)
        self.get_courses()
        self.add_user_info()
        self.settingsWindow = Settings(self.fullname, self.SID, self.email, self.database)
        self.preEventsLen = len(events)
        self.add_events_GUI()
        self.refresh = False
        self.refreshNotes = False
        timer = QTimer(self)
        timer.timeout.connect(self.add_time_date)
        timer.start(100)
    
    def add_event(self):
        self.addEventPopUp.show()
        self.addEventPopUp.pushButton.clicked.connect(self.addEventPopUp.addEvent)
    
    def go_to(self, place):
        self.widget.setCurrentIndex(self.window_indexes[place])
        self.refresh = True
        
    def add_events_GUI(self):
        for event in self.events:
            button = QPushButton()
            d = event[0]
            date_str = d.strftime('%Y-%m-%d')
            button.setText("Name: " + event[2] + "\nDue: " + date_str)
            self.formLayout.addRow(button)

    def logout(self):
        self.widget.close()
        self.loginWidget.setCurrentIndex(0)
        self.loginWidget.show()

    def reset_button_labels(self):
        for button in self.buttonContainer.children():
            if "button" in button.objectName():
                button.setText("")
    
    def get_courses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Courses WHERE SID=" + str(self.SID))
        self.add_courses_timetable(cursor)

    def add_courses_timetable(self, cursor):
        for row in cursor:
            self.courses.append(row)
            course_id = row[1]
            course_name = row[2]
            course_day = row[3].lower()
            course_link = row[6]
            start = row[4].split(":")[0]
            end = row[5].split(":")[0]
            duration = int(end) - int(start)
            for btn in self.buttonContainer.children():
                btn_info = btn.objectName().split("_")
                if "button" not in btn_info:
                    continue
                btn_start = btn_info[1]
                btn_day = btn_info[0].lower()
                if course_day == btn_day and start == btn_start:
                    btn.setText("%s\n%s" % (course_id, course_name))
                    self.usedButtons[btn.objectName()] = course_link
                if course_day == btn_day and int(end)-1 == int(btn_start):
                    btn.setText("%s\n%s" % (course_id, course_name))
                    self.usedButtons[btn.objectName()] = course_link
                if course_day == btn_day and int(btn_start) > int(start) and int(btn_start) - int(start) < duration:
                    btn.setText("%s\n%s" % (course_id, course_name))
                    self.usedButtons[btn.objectName()] = course_link
        for btn in self.buttonContainer.children():
            if btn.objectName() in self.usedButtons:
                btn.clicked.connect(self.launch_course)

    def launch_course(self):
        try:
            driver = webdriver.Chrome("./chromedriver")
            driver.get(self.usedButtons[self.sender().objectName()])
        except:
            pass
        
    def add_user_info(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Student WHERE SID=" + str(self.SID))
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
            button.setText("Name: " + self.events[len(self.events)-1][2] + "\nDue: " + str(self.events[len(self.events)-1][0]))
            self.formLayout.addRow(button)
        if self.widget.currentIndex() == self.window_indexes["dashboard"] and self.refresh:
            self.reset_button_labels()
            self.get_courses()
            self.refresh = False
        if self.refreshNotes:
            for i in reversed(range(self.formLayout.count())): 
                self.formLayout.itemAt(i).widget().setParent(None)
            self.add_events_GUI()
            self.refreshNotes = False
    
    def goto_settings(self):
        self.settingsWindow.show()
        self.settingsWindow.setWindowTitle("Settings")
                


