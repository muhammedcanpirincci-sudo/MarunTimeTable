import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from coursePopUp import *
from course_add_pop_up import *
from PyQt5.QtCore import QTimer, QTime, Qt, QDate
from PyQt5.QtGui import QPixmap
from settings import *



class Courses(QDialog):
    def __init__(self, widget, loginWidget, window_indexes, database,SID, settingsWindow):
        super(Courses, self).__init__()
        loadUi("ui/mttCourses.ui", self)
        self.widget = widget
        self.loginWidget = loginWidget
        self.window_indexes = window_indexes
        self.goBackButton.clicked.connect(lambda: self.widget.setCurrentIndex(self.window_indexes["dashboard"]))
        self.eventsButton.clicked.connect(lambda: self.widget.setCurrentIndex(self.window_indexes["events"]))
        self.notesButton.clicked.connect(lambda: self.widget.setCurrentIndex(self.window_indexes["notes"]))
        self.logoutButton.clicked.connect(self.logout)
        self.conn = pyodbc.connect(database)
        self.window_indexes = window_indexes
        self.database = database
        self.SID=SID
        self.edit = coursePopUp(database)
        self.fullname = ''
        self.email = ''
        self.settingButton.clicked.connect(self.goto_settings)
        self.Button_List = []
        self.ID_List = []
        self.cursor2 = self.conn.cursor()
        self.new_object2 = course_add_pop_up(self.widget, self.window_indexes, self.database, self.SID)
        self.add_user_info()
        self.authenticate()
        self.addCourseButton.clicked.connect(self.on_click2)
        self.new_object2.pushButton.clicked.connect(self.buttons_update)
        self.settingsWindow = settingsWindow
        self.refresh = False
        timer = QTimer(self)
        timer.timeout.connect(self.add_time_date)
        timer.start(100)

    def authenticate(self):
        self.my_button_group = QButtonGroup()
        self.formLayout = self.formLayout_4
        self.buttons_update()

        for i in self.Button_List:
            self.my_button_group.addButton(i)

    def buttons_update(self):
        self.flag=1
        self.Button_List = []
        self.ID_List = []

        for i in reversed(range(self.formLayout.count())): 
            self.formLayout.itemAt(i).widget().setParent(None)

        self.cursor2.execute("SELECT COUNT(*) FROM Courses WHERE SID=%s" % self.SID)
        len = int(self.cursor2.fetchone()[0])

        for i in range(len):
            self.cursor2.execute("SELECT * FROM Courses WHERE SID=%s" %self.SID)

            fetch_tuple = [str(i) for i in self.cursor2.fetchall()[i]]
            button = QPushButton(fetch_tuple[2])
            button.setObjectName(fetch_tuple[0])
            button.clicked.connect(self.on_click)
            self.Button_List.append(button)
            self.ID_List.append(button.objectName())
            self.formLayout.addRow(self.Button_List[i])
        


    def on_click(self):  
        courseID = self.sender().objectName()
        self.edit = coursePopUp(self.database)
        self.edit.instertion(courseID)
        self.edit.show()


    def on_click2(self):
        self.new_object2.show()

    def logout(self):
        self.widget.close()
        self.loginWidget.setCurrentIndex(0)
        self.loginWidget.show()

    def add_user_info(self):
        self.cursor2.execute("SELECT * FROM Student WHERE SID=%s" % str(self.SID))
        for row in self.cursor2:
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
        self.refresh = self.edit.refresh
        if self.refresh:
            self.buttons_update()
            self.refresh = False
            self.edit.refresh = False
    
    def goto_settings(self):
        self.settingsWindow.show()
        self.settingsWindow.setWindowTitle("Settings")