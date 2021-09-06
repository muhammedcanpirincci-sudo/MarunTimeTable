import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFormLayout, QLabel, QGroupBox, QPushButton, QVBoxLayout, \
    QScrollArea, QMainWindow, QTableWidgetItem, QHeaderView, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime
import pyodbc
from PyQt5 import QtGui

class coursePopUp(QDialog):
    def __init__(self, database):
        super(coursePopUp, self).__init__()
        loadUi("ui/mttAddCoursePopUp.ui", self)
        self.conn = pyodbc.connect(database)
        self.refresh = False
        self.database = database
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.cursor = self.conn.cursor()
        self.add_days()

    def add_days(self):
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Sunday', 'Saturday']:
            self.comboBox.addItem(day)

    def apply(self, ID):
        course_id = self.textEdit.toPlainText()
        name = self.textEdit_2.toPlainText()
        Course_time_day = self.comboBox.currentText()
        Course_Time_StartHour = self.timeEdit.time().toString()
        Course_Time_EndHour = self.timeEdit_2.time().toString()
        CourseLink = self.textEdit_4.toPlainText()
        Resource_Link = self.textEdit_5.toPlainText()
        Professor_Email = self.textEdit_6.toPlainText()
        Ta_Email = self.textEdit_7.toPlainText()
        if len(name) == 0 or len(Course_time_day) == 0 or len(Course_Time_StartHour) == 0 or \
                len(Course_Time_EndHour) == 0 or len(CourseLink) == 0:
            self.error = Error("You left important fields empty")
            self.error.show()
            return

        self.cursor.execute(
            "UPDATE Courses \
            SET Course_Id='%s', \
                name='%s', \
                Course_Time_Day='%s', \
                Course_Time_StartHour='%s',\
                Course_Time_EndHour='%s', \
                CourseLink='%s',\
                Resource_Link='%s',\
                Professor_Email='%s',\
                Ta_Email='%s' \
            WHERE ID='%s'" %
            (course_id, name, Course_time_day, Course_Time_StartHour, Course_Time_EndHour,
             CourseLink, Resource_Link, Professor_Email, Ta_Email, ID))
        self.cursor.commit()
        self.refresh = True
        self.close()


    def instertion(self, ID):
        self.cursor.execute("SELECT * FROM Courses WHERE ID='%s'" % ID)
        for row in self.cursor:
            self.textEdit.setText(row[1])
            self.textEdit_2.setText(row[2])
            start = QTime(int(row[4].split(":")[0]), 0)
            end = QTime(int(row[5].split(":")[0]), 0)
            self.timeEdit.setTime(start)
            self.timeEdit_2.setTime(end)
            self.textEdit_4.setText(row[6])
            self.textEdit_5.setText(row[7])
            self.textEdit_6.setText(row[8])
            self.textEdit_7.setText(row[9])
        self.pushButton.setText("Apply")
        self.pushButton.clicked.connect(lambda:self.apply(ID))

