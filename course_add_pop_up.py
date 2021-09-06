import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFormLayout, QLabel, QGroupBox, QPushButton, QVBoxLayout, \
    QScrollArea, QMainWindow, QTableWidgetItem, QHeaderView, QWidget
from PyQt5.uic import loadUi
import pyodbc
from PyQt5 import QtGui

class course_add_pop_up(QDialog):
    def __init__(self, widget,window_indexes, database,SID):
        super(course_add_pop_up, self).__init__()
        loadUi("ui/mttAddCoursePopUp.ui", self)
        self.window_indexes = window_indexes
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.widget=widget
        self.conn = pyodbc.connect(database)
        self.window_indexes = window_indexes
        self.add_days()
        self.SID=SID
        self.database = database
        self.cursor = self.conn.cursor()
        self.original_list = []
        self.pushButton.clicked.connect(self.instertion)

    def add_days(self):
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Sunday', 'Saturday']:
            self.comboBox.addItem(day)

    def instertion(self):
        course_id = self.textEdit.toPlainText()
        name = self.textEdit_2.toPlainText()
        Course_time_day = self.comboBox.currentText()
        Course_Time_StartHour = self.timeEdit.time().toString()
        Course_Time_EndHour = self.timeEdit_2.time().toString()
        CourseLink = self.textEdit_4.toPlainText()
        Resource_Link = self.textEdit_5.toPlainText()
        Professor_Email = self.textEdit_6.toPlainText()
        Ta_Email = self.textEdit_7.toPlainText()
        print(course_id, name, Course_time_day, Course_Time_StartHour, Course_Time_EndHour,
              CourseLink, Resource_Link, Professor_Email, Ta_Email)
        if len(name) == 0 or len(Course_time_day) == 0 or len(Course_Time_StartHour) == 0 or \
                len(Course_Time_EndHour) == 0 or len(CourseLink) == 0:
            self.error = Error("You left important fields empty")
            self.error.show()
            return

        self.cursor.execute(
            "INSERT INTO Courses(Course_Id,name,Course_Time_Day,Course_Time_StartHour,Course_Time_EndHour, \
                CourseLink,Resource_Link,Professor_Email,Ta_Email,SID) values(?,?,?,?,?,?,?,?,?,?)",
            (course_id, name, Course_time_day, Course_Time_StartHour, Course_Time_EndHour,
             CourseLink, Resource_Link, Professor_Email, Ta_Email, self.SID))

        self.conn.commit()

        print("in add course")
        self.cursor.execute("SELECT * FROM Courses")
        self.close()
        



