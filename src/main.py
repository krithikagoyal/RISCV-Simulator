"""
The project is developed as part of Computer Architecture class.
Project Name: Functional Simulator for subset of RISC-V Processor

-------------------------------------------------
| Developer's Name   | Developer's Email ID     |
|-----------------------------------------------|
| Akhil Arya         | 2019csb1066@iitrpr.ac.in |
| Harshwardhan Kumar | 2019csb1089@iitrpr.ac.in |
| Krithika Goyal     | 2019csb1094@iitrpr.ac.in |
| Rhythm Jain        | 2019csb1111@iitrpr.ac.in |
| Tarun Singla       | 2019csb1126@iitrpr.ac.in |
-------------------------------------------------
"""

# main.py
# Purpose of this file: This file handles the input and output, and invokes the simulator.

from myRISCVSim import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog
import sys
import time

filename = ""
class Ui_takeInput(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(807, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 280, 161, 61))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 150, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 807, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Choose File"))
        self.label.setText(_translate("MainWindow", "Choose the input file "))
        self.pushButton.clicked.connect(self.pushButton_handler)

    def pushButton_handler(self):
        self.openDialogBox()
    
    def openDialogBox(self):
        global filename
        filename = QFileDialog.getOpenFileName()
        MainWindow.close()


class Ui_displayOutput(object):
    def setupUi(self, MainWindow, filename):
        MainWindow.width = 1900
        MainWindow.height = 1000
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(890, 0, 141, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 40, MainWindow.width, MainWindow.height - 100))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)        
        self.tableWidget.setRowCount(100) # changed
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setItem(0, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setItem(0, 1, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tableWidget.setColumnWidth(0, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(1, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(2, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(3, int(MainWindow.width / 4) - 30)
        self.retranslateUi(MainWindow, filename)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Data Memory"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ADDRESS"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "HEX"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "BINARY"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "DECIMAL"))

        f = open(filename, "r")
        f = f.readlines()
        for i in range(len(f)):
            f[i] = f[i].split()
        for i in range(100):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][0]))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", hex(int(f[i][1], 16))))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 2, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", bin(int(f[i][1], 16))))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 3, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", str(int(f[i][1], 16))))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_takeInput()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    # set .mc file
    prog_mc_file = filename[0]

    # reset the processor
    reset_proc()

    # load the program memory
    load_program_memory(prog_mc_file)

    # run the simulator
    run_RISCVsim()

    MainWindow2 = QtWidgets.QMainWindow()
    ui = Ui_displayOutput()
    ui.setupUi(MainWindow2, "src/data.mc")
    MainWindow2.show()
    sys.exit(app.exec_())