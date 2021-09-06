import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pyodbc
from courses import *
from dashboard import *
from events import *
from notes import *

class Login(QDialog):

    def __init__(self, widget, window_indexes, database):
        super(Login, self).__init__()
        loadUi("ui/mttLogin.ui", self)
        self.conn = pyodbc.connect(database)
        self.loginWidget = widget
        self.dashboardWidget = QtWidgets.QStackedWidget()
        self.window_indexes = window_indexes
        self.registerButton.clicked.connect(self.goto_register)
        self.loginButton.clicked.connect(self.authenticate)
        self.reset_login()
        self.database=database
        self.SID=0
        self.events = []

    def get_events(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Event WHERE SID=%s" % str(self.SID))
        for row in cursor:
            self.events.append([row[1], row[2], row[3], row[4], row[5], row[0]])
        self.preEventsLen = len(self.events)

    def reset_login(self):
        self.errorLabel.setText("")  # initially makes login error invisible
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

    def goto_register(self):
        self.loginWidget.setCurrentIndex(self.window_indexes["register"])

    def login(self):
        windows_num=0
        self.events = []
        self.get_events()
        self.dashboardWidget = QtWidgets.QStackedWidget()

        # Dashboard UI
        dashboardWindow = Dashboard(self.dashboardWidget, self.loginWidget, self.window_indexes, self.database, self.SID, self.events)
        self.dashboardWidget.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.dashboardWidget.setWindowTitle("MarunTimeTable")
        self.dashboardWidget.addWidget(dashboardWindow)
        self.window_indexes["dashboard"] = windows_num
        self.reset_login()
        self.loginWidget.close()
        self.dashboardWidget.setCurrentIndex(self.window_indexes["dashboard"])
        self.dashboardWidget.setMinimumSize(810, 410)
        self.dashboardWidget.show()

        # Courses UI
        coursersWindow = Courses(self.dashboardWidget, self.loginWidget, self.window_indexes, 
        self.database, self.SID, dashboardWindow.settingsWindow)
        self.dashboardWidget.addWidget(coursersWindow)
        windows_num+=1
        self.window_indexes["courses"] = windows_num

        # Events UI
        eventsWindow = Events(self.dashboardWidget, self.loginWidget, self.window_indexes, 
        self.database, self.SID, dashboardWindow.settingsWindow, self.events, dashboardWindow)
        self.dashboardWidget.addWidget(eventsWindow)
        windows_num+=1
        self.window_indexes["events"] = windows_num

        # Notes UI
        notesWindow = Notes(self.dashboardWidget, self.loginWidget, self.window_indexes, 
        self.database, self.SID, dashboardWindow.settingsWindow)
        self.dashboardWidget.addWidget(notesWindow)
        windows_num+=1
        self.window_indexes["notes"] = windows_num

    def authenticate(self):
        print(self.lineEdit_2.text())
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Student")
        user_found = False
        for row in cursor:
            print(f'row = ', row[0], row[3], row[4])
            if (self.lineEdit.text() == row[3] and self.lineEdit_2.text() == row[4]) or\
                (self.lineEdit.text() == str(row[0]) and self.lineEdit_2.text() == row[4]) :
                self.SID=row[0]
                user_found = True
                break
        cursor.commit()
        if user_found:
            self.login()
        else:
            self.errorLabel.setText("You've entered incorrect credentials")