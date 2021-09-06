import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtGui

class Error(QDialog):
    def __init__(self, message):
        super(Error, self).__init__()
        loadUi("ui/mttError.ui", self)
        self.label.setText(message)
        self.pushButton.clicked.connect(self.close)
        self.setWindowTitle("Error")
        self.setWindowIcon(QtGui.QIcon('logo/logo_only_transparent.png'))
    
   
