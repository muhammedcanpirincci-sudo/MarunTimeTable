import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from changeName import *
from changeEmail import *
from changePassword import *
from PIL import Image
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui


class Settings(QDialog):
    def __init__(self, fullname, SID, email, database):
        super(Settings, self).__init__()
        loadUi("ui/mttSettings.ui", self)
        self.fullname = fullname
        self.SID = SID
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
        self.userEmail = email
        self.database = database
        self.changeNameButton.clicked.connect(self.goto_change_name)
        self.changeEmailButton.clicked.connect(self.goto_change_email)
        self.changePasswordButton.clicked.connect(self.goto_change_password)
        self.changePictureButton.clicked.connect(self.change_picture)
        timer = QTimer(self)
        timer.timeout.connect(self.refreshWindow)
        timer.start(100)
        self.changeNameWindow = ChangeName(self.SID, self.database, self.fullname)
        self.changeEmailWindow = ChangeEmail(self.SID, self.database, self.userEmail)
        self.changePasswordWindow = ChangePassword(self.SID, self.database)

    def goto_change_name(self):
        self.changeNameWindow.setWindowTitle("New Name")
        self.changeNameWindow.show()

    def goto_change_email(self):
        self.changeEmailWindow.setWindowTitle("New Email")
        self.changeEmailWindow.show()

    def goto_change_password(self):
        self.changePasswordWindow.setWindowTitle("New Password")
        self.changePasswordWindow.show()
    
    def change_picture(self):
        fileName, fileType = QFileDialog.getOpenFileName(self,"Select a New Profile Picture", 
        "","Image Files (*.png *.jpg *jpeg)")
        try:
            im1 = Image.open(fileName)
            im1.save("profile.png")
        except:
            pass    

    def refreshWindow(self):
        self.fullname = self.changeNameWindow.fullname
        self.userEmail = self.changeEmailWindow.userEmail
        self.nameSurname.setText(self.fullname)
        self.sid.setText(str(self.SID))
        self.email.setText(self.userEmail)
        pix = QPixmap("profile.png")
        self.picture.setPixmap(pix)
        
        



        