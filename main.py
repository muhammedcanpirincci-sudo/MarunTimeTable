import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtGui
from PyQt5.uic import loadUi
import pyodbc
from login import *
from register import *
from courses import *
from dashboard import *
from events import *
from notes import *
import hashlib

window_indexes = {}  # Key: window_name, value: window_index, ex. key: "login", value: 1

sam_database = ("Driver={SQL Server};" +
    "Server=DESKTOP-69M9PD0;" +
    "Database=mttDatabase;" +
    "Trusted_Connection=yes;")

basil_database = ("Driver={SQL Server};" +
    "Server=DESKTOP-28COGFI;" +
    "Database=mttDatabase;" +
    "Trusted_Connection=yes;")

muhammed_database = ("Driver={SQL Server};" +
    "Server=DESKTOP-NF57O1P;" +
    "Database=mttDatabase;" +
    "Trusted_Connection=yes;")


database = basil_database # Sam, everytime you run this, just set database to sam_database

conn = pyodbc.connect(database)

def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student")
    for row in cursor:
        print(f'row = ', row[3], row[4])
    print()


read(conn)

def launch_login_add_ui(widget):
    windows_num = 0 # Number of windows of the program

    # Login UI
    loginWindow = Login(widget, window_indexes, database)
    widget.addWidget(loginWindow)
    window_indexes["login"] = 0

    # Register UI
    registerWindow = Register(widget, window_indexes, database)
    widget.addWidget(registerWindow)
    windows_num+=1
    window_indexes["register"] = windows_num


    widget.setMaximumSize(480,600)
    widget.setMinimumSize(480,600)
    widget.show()

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
widget.setWindowTitle("MarunTimeTable")
try:
    launch_login_add_ui(widget)
    app.exec()
except:
    pass



