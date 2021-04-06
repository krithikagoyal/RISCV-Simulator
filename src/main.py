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

from myRISCVSim import run_RISCVsim, reset_proc, load_program_memory
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog
import sys
import time
import os

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
        self.pushButton.clicked.connect(lambda: self.pushButton_handler(MainWindow))

    def pushButton_handler(self, MainWindow):
        self.openDialogBox(MainWindow)
    
    def openDialogBox(self, MainWindow):
        global filename
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.join(path, 'test')
        filename = QFileDialog.getOpenFileName(MainWindow, 'Open file', path)
        MainWindow.close()

class display_data(object):
    def setupUi(self, MainWindow, filename):
        MainWindow.width = 1900
        MainWindow.height = 1000
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(880, 50, 200, 35))
        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(820, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(950, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.register_button.clicked.connect(self.show_register_data)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 95, MainWindow.width, MainWindow.height - 100))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)        
        self.tableWidget.setRowCount(8192) # changed
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
        self.tableWidget.setColumnWidth(0, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(1, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(2, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(3, int(MainWindow.width / 4) - 30)
        self.retranslateUi(MainWindow, filename)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_register_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 1)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Data Memory"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
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
        for i in range(8192):
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

class display_register(object):
    def setupUi(self, MainWindow, filename):
        MainWindow.width = 1900
        MainWindow.height = 1000
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(850, 50, 200, 35))
        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(820, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(950, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.memory_button.clicked.connect(self.show_memory_data)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 95, MainWindow.width, MainWindow.height - 100))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)        
        self.tableWidget.setRowCount(32) # changed
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
        self.tableWidget.setColumnWidth(0, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(1, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(2, int(MainWindow.width / 4) - 30)
        self.tableWidget.setColumnWidth(3, int(MainWindow.width / 4) - 30)
        self.retranslateUi(MainWindow, filename)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_memory_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() - 1)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Register Memory"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
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
        for i in range(32):
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

    # display the data
    MainWindow2 = QtWidgets.QWidget()
    MainWindow3 = QtWidgets.QWidget()
    ui1 = display_data()
    ui1.setupUi(MainWindow2, "data_out.mc")
    ui2 = display_register()
    ui2.setupUi(MainWindow3, "data_out.mc")
    widgets = QtWidgets.QStackedWidget()
    widgets.setFixedHeight(1000)
    widgets.setFixedWidth(1900)
    widgets.addWidget(MainWindow2)
    widgets.addWidget(MainWindow3)
    widgets.show()
    sys.exit(app.exec_())