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
# Purpose of this file: This file controls the Graphical User Interface(GUI).

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog
import time
import os

# Knobs
pipelining_enabled = False
forwarding_enabled = False
print_registers_each_cycle = False
print_specific_pipeline_registers = False
print_pipeline_registers = False
number = -1

# Data cache parameters
data_cache_size = 128
data_cache_block_size = 16 # Word is 4B
data_cache_associativity = 2 # 0/1/2[FA/DM/SA]
data_cache_ways = 2

# Instruction cache parameters
instruction_cache_size = 128
instruction_cache_block_size = 16 # Word is 4B
instruction_cache_associativity = 2 # 0/1/2[FA/DM/SA]
instruction_cache_ways = 2


class Ui_takeInput(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(807, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(345, 140, 161, 61))
        self.pushButton.setObjectName("pushButton")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(345, 470, 161, 61))
        self.run.setObjectName("pushButton_run")
        font = QtGui.QFont()
        font.setPointSize(16)
        font2 = QtGui.QFont()
        font2.setPointSize(12)

        self.pipelining_enabled = QtWidgets.QCheckBox(self.centralwidget)
        self.pipelining_enabled.setGeometry(QtCore.QRect(180, 245, 500, 30))
        self.pipelining_enabled.setFont(font2)

        self.forwarding_enabled = QtWidgets.QCheckBox(self.centralwidget)
        self.forwarding_enabled.setGeometry(QtCore.QRect(180, 275, 500, 30))
        self.forwarding_enabled.setFont(font2)

        self.print_registers_each_cycle = QtWidgets.QCheckBox(self.centralwidget)
        self.print_registers_each_cycle.setGeometry(QtCore.QRect(180, 305, 500, 30))
        self.print_registers_each_cycle.setFont(font2)

        self.print_pipeline_registers = QtWidgets.QCheckBox(self.centralwidget)
        self.print_pipeline_registers.setGeometry(QtCore.QRect(180, 335, 500, 30))
        self.print_pipeline_registers.setFont(font2)

        self.print_specific_pipeline_registers = QtWidgets.QCheckBox(self.centralwidget)
        self.print_specific_pipeline_registers.setGeometry(QtCore.QRect(180, 365, 500, 30))
        self.print_specific_pipeline_registers.setFont(font2)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 80, 301, 41))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.pushButton.setText(_translate("MainWindow", "Choose File"))
        self.run.setText(_translate("MainWindow", "Next"))

        self.label.setText(_translate("MainWindow", "Choose the input file "))
        self.pushButton.clicked.connect(lambda: self.pushButton_handler(MainWindow))
        self.run.clicked.connect(lambda: self.run_handler(MainWindow))

        self.pipelining_enabled.setText(_translate("MainWindow", "Enable pipelining"))
        self.forwarding_enabled.setText(_translate("MainWindow", "Enable forwarding"))
        self.print_registers_each_cycle.setText(_translate("MainWindow", "Enable printing registers in each cycle"))
        self.print_pipeline_registers.setText(_translate("MainWindow", "Enable printing pipeling registers"))
        self.print_specific_pipeline_registers.setText(_translate("MainWindow", "Enable printing specific pipeline registers"))

        self.pipelining_enabled.stateChanged.connect(self.checked_pipelining_enabled)
        self.forwarding_enabled.stateChanged.connect(self.checked_forwarding_enabled)
        self.print_registers_each_cycle.stateChanged.connect(self.checked_print_registers_each_cycle)
        self.print_pipeline_registers.stateChanged.connect(self.checked_print_pipeline_registers)
        self.print_specific_pipeline_registers.stateChanged.connect(lambda: self.checked_print_specific_pipeline_registers(MainWindow))

    def checked_pipelining_enabled(self):
        global pipelining_enabled
        pipelining_enabled = not pipelining_enabled

    def checked_forwarding_enabled(self):
        global forwarding_enabled
        forwarding_enabled = not forwarding_enabled

    def checked_print_registers_each_cycle(self):
        global print_registers_each_cycle
        print_registers_each_cycle = not print_registers_each_cycle

    def checked_print_pipeline_registers(self):
        global print_pipeline_registers
        print_pipeline_registers = not print_pipeline_registers

    def checked_print_specific_pipeline_registers(self, MainWindow):
        global print_specific_pipeline_registers, number
        print_specific_pipeline_registers = not print_specific_pipeline_registers
        if print_specific_pipeline_registers:
            number, done2 = QtWidgets.QInputDialog.getInt(MainWindow, 'Input Number', 'Enter the instruction number:')
        else:
            number = -1

    def pushButton_handler(self, MainWindow):
        self.openDialogBox(MainWindow)

    def openDialogBox(self, MainWindow):
        global filename
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, 'test')
        filename = QFileDialog.getOpenFileName(MainWindow, 'Open file', path, "*.mc")

    def run_handler(self, MainWindow):
        w.setCurrentIndex(w.currentIndex() + 1)

class Ui_takeDataCacheInput(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(875, 660)

        font = QtGui.QFont()
        font.setPointSize(16)

        font2 = QtGui.QFont()
        font2.setPointSize(11)

        font3 = QtGui.QFont()
        font3.setPointSize(9)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 80, 561, 61))
        self.label.setObjectName("label")
        self.label.setFont(font)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(285, 190, 120, 30))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 240, 170, 30))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(130, 180, 16, 16))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_6.setFont(font2)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(400, 330, 171, 23))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setFont(font3)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(400, 370, 161, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setFont(font3)
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(400, 290, 151, 23))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setFont(font3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 480, 141, 51))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 290, 181, 30))
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font2)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(400, 195, 113, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 245, 113, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 480, 151, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 875, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.go_next)
        self.pushButton_2.clicked.connect(self.go_back)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.radioButton.toggled.connect(self.fully_associative)
        self.radioButton_2.toggled.connect(lambda: self.set_associative(MainWindow))
        self.radioButton_3.toggled.connect(self.direct_mapped)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Enter data cache specifications:"))
        self.label_2.setText(_translate("MainWindow", "Cache size:"))
        self.label_3.setText(_translate("MainWindow", "Cache block size:"))
        self.radioButton.setText(_translate("MainWindow", "Fully associative"))
        self.radioButton_2.setText(_translate("MainWindow", "Set associative"))
        self.radioButton_3.setText(_translate("MainWindow", "Direct mapped"))
        self.pushButton.setText(_translate("MainWindow", "Next"))
        self.label_4.setText(_translate("MainWindow", "Select associativity:"))
        self.pushButton_2.setText(_translate("MainWindow", "Back"))

    def fully_associative(self):
        global data_cache_associativity
        if self.radioButton.isChecked():
            data_cache_associativity = 0

    def set_associative(self, MainWindow):
        global data_cache_associativity, data_cache_ways
        if self.radioButton_2.isChecked():
            data_cache_ways, done2 = QtWidgets.QInputDialog.getInt(MainWindow, 'Input Number', 'Data cache ways:')
            data_cache_associativity = 2

    def direct_mapped(self):
        global data_cache_associativity
        if self.radioButton_3.isChecked():
            data_cache_associativity = 1

    def go_next(self):
        global data_cache_size, data_cache_block_size
        data_cache_size = 128
        data_cache_block_size = 16 # Word is 4B
        w.setCurrentIndex(w.currentIndex() + 1)

    def go_back(self):
        global data_cache_size, data_cache_block_size
        data_cache_size = 128
        data_cache_block_size = 16 # Word is 4B
        w.setCurrentIndex(w.currentIndex() - 1)

class Ui_takeInstructionCacheInput(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(875, 660)

        font = QtGui.QFont()
        font.setPointSize(16)

        font2 = QtGui.QFont()
        font2.setPointSize(11)

        font3 = QtGui.QFont()
        font3.setPointSize(9)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 80, 561, 61))
        self.label.setObjectName("label")
        self.label.setFont(font)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(285, 190, 120, 30))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 240, 170, 30))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(130, 180, 16, 16))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_6.setFont(font2)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(400, 330, 171, 23))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setFont(font3)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(400, 370, 161, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setFont(font3)
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(400, 290, 151, 23))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setFont(font3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 480, 141, 51))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 290, 181, 30))
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font2)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(400, 195, 113, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 245, 113, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 480, 151, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 875, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.go_next)
        self.pushButton_2.clicked.connect(self.go_back)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.radioButton.toggled.connect(self.fully_associative)
        self.radioButton_2.toggled.connect(lambda: self.set_associative(MainWindow))
        self.radioButton_3.toggled.connect(self.direct_mapped)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Enter instruction cache specifications:"))
        self.label_2.setText(_translate("MainWindow", "Cache size:"))
        self.label_3.setText(_translate("MainWindow", "Cache block size:"))
        self.radioButton.setText(_translate("MainWindow", "Fully associative"))
        self.radioButton_2.setText(_translate("MainWindow", "Set associative"))
        self.radioButton_3.setText(_translate("MainWindow", "Direct mapped"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
        self.label_4.setText(_translate("MainWindow", "Select associativity:"))
        self.pushButton_2.setText(_translate("MainWindow", "Back"))

    def fully_associative(self):
        global instruction_cache_associativity
        if self.radioButton.isChecked():
            instruction_cache_associativity = 0

    def set_associative(self, MainWindow):
        global instruction_cache_associativity, instruction_cache_ways
        if self.radioButton_2.isChecked():
            instruction_cache_ways, done2 = QtWidgets.QInputDialog.getInt(MainWindow, 'Input Number', 'Instruction cache ways:')
            instruction_cache_associativity = 2

    def direct_mapped(self):
        global instruction_cache_associativity
        if self.radioButton_3.isChecked():
            instruction_cache_associativity = 1

    def go_next(self):
        global instruction_cache_size, instruction_cache_block_size
        instruction_cache_size = self.lineEdit.text()
        instruction_cache_block_size = self.lineEdit_2.text() # Word is 4B
        w.close()

    def go_back(self):
        global instruction_cache_size, instruction_cache_block_size
        instruction_cache_size = self.lineEdit.text()
        instruction_cache_block_size = self.lineEdit_2.text() # Word is 4B
        w.setCurrentIndex(w.currentIndex() - 1)

class display_data(object):
    def setupUi(self, MainWindow, filename):
        MainWindow.width = 1900
        MainWindow.height = 970
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(840, 50, 200, 35))

        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(660, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(790, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.data_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_hazard_button.setGeometry(QtCore.QRect(920, 3, 125, 40))
        self.data_hazard_button.setObjectName("data_hazrad")
        self.control_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.control_hazard_button.setGeometry(QtCore.QRect(1050, 3, 125, 40))
        self.control_hazard_button.setObjectName("control_hazrad")

        self.register_button.clicked.connect(self.show_register_data)
        self.control_hazard_button.clicked.connect(self.show_control_hazard)
        self.data_hazard_button.clicked.connect(self.show_data_hazard)

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

    def show_data_hazard(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 2)

    def show_control_hazard(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 3)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Memory Data"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.data_hazard_button.setText(_translate("MainWindow", "Data Hazard"))
        self.control_hazard_button.setText(_translate("MainWindow", "Control Hazard"))
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
        MainWindow.height = 970
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(850, 50, 200, 35))

        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(660, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(790, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.data_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_hazard_button.setGeometry(QtCore.QRect(920, 3, 125, 40))
        self.data_hazard_button.setObjectName("data_hazrad")
        self.control_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.control_hazard_button.setGeometry(QtCore.QRect(1050, 3, 125, 40))
        self.control_hazard_button.setObjectName("control_hazrad")

        self.memory_button.clicked.connect(self.show_memory_data)
        self.data_hazard_button.clicked.connect(self.show_data_hazard)
        self.control_hazard_button.clicked.connect(self.show_control_hazard)

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

    def show_data_hazard(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 1)

    def show_control_hazard(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 2)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Register Data"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.data_hazard_button.setText(_translate("MainWindow", "Data Hazard"))
        self.control_hazard_button.setText(_translate("MainWindow", "Control Hazard"))
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

class display_data_hazard(object):
    def setupUi(self, MainWindow, l):
        MainWindow.width = 1900
        MainWindow.height = 970
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(760, 50, 400, 35))

        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(660, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(790, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.data_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_hazard_button.setGeometry(QtCore.QRect(920, 3, 125, 40))
        self.data_hazard_button.setObjectName("data_hazrad")
        self.control_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.control_hazard_button.setGeometry(QtCore.QRect(1050, 3, 125, 40))
        self.control_hazard_button.setObjectName("control_hazrad")

        self.memory_button.clicked.connect(self.show_memory_data)
        self.register_button.clicked.connect(self.show_register_data)
        self.control_hazard_button.clicked.connect(self.show_control_hazard)

        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(290, 95, 700, 40))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(260, 95, 31, 40))
        self.plainTextEdit_2.setStyleSheet("background-color: rgb(0, 255, 149);")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(1000, 95, 31, 40))
        self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 252, 105);")
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(1030, 95, 700, 40))
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.plainTextEdit_4.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 130, MainWindow.width, MainWindow.height - 125))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(l)) # changed
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.setColumnWidth(0, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(1, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(2, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(3, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(4, int(MainWindow.width / 5) - 20)
        self.retranslateUi(MainWindow, l)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_memory_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() - 2)

    def show_register_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() - 1)

    def show_control_hazard(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 1)

    def retranslateUi(self, MainWindow, l):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Colors representing Data Hazard"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.data_hazard_button.setText(_translate("MainWindow", "Data Hazard"))
        self.control_hazard_button.setText(_translate("MainWindow", "Control Hazard"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Stall happened because it was dependent on some previous instruction"))
        self.plainTextEdit_4.setPlainText(_translate("MainWindow", "Stall happened beacuse some next instruction was dependent on it"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Fetch"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Decode"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Execute"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Memory"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Write back"))

        f = l
        for i in range(len(f)):
            if forwarding_enabled and pipelining_enabled:
                 self.tableWidget.setRowHeight(i, 80)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][0]))
            if '\n' in f[i][0] and forwarding_enabled and pipelining_enabled:
                item.setForeground(QtGui.QColor(36, 53, 181))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][1]))
            if '\n' in f[i][1] and forwarding_enabled and pipelining_enabled:
                item.setForeground(QtGui.QColor(36, 53, 181))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 2, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][2]))
            if '\n' in f[i][2] and forwarding_enabled and pipelining_enabled:
                item.setForeground(QtGui.QColor(36, 53, 181))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 3, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][3]))
            if '\n' in f[i][3] and forwarding_enabled and pipelining_enabled:
                item.setForeground(QtGui.QColor(36, 53, 181))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 4, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][4]))
            if '\n' in f[i][4] and forwarding_enabled and pipelining_enabled:
                item.setForeground(QtGui.QColor(36, 53, 181))
            if f[i][5]['who'] != -1:
                self.tableWidget.item(i, f[i][5]['who']).setBackground(QtGui.QColor(0, 255, 149))
                self.tableWidget.item(i, f[i][5]['from_whom']).setBackground(QtGui.QColor(255, 252, 105))

class display_control_hazard(object):
    def setupUi(self, MainWindow, l, control_hazard_signals):
        MainWindow.width = 1900
        MainWindow.height = 970
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(750, 50, 400, 35))

        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(660, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(790, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.data_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_hazard_button.setGeometry(QtCore.QRect(920, 3, 125, 40))
        self.data_hazard_button.setObjectName("data_hazrad")
        self.control_hazard_button = QtWidgets.QPushButton(self.centralwidget)
        self.control_hazard_button.setGeometry(QtCore.QRect(1050, 3, 125, 40))
        self.control_hazard_button.setObjectName("control_hazrad")

        self.memory_button.clicked.connect(self.show_memory_data)
        self.register_button.clicked.connect(self.show_register_data)
        self.data_hazard_button.clicked.connect(self.show_data_hazard)

        # representing colors
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(590, 95, 200, 40))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(560, 95, 31, 40))
        self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 94, 94);")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(820, 95, 31, 40))
        self.plainTextEdit_3.setStyleSheet("background-color: rgb(247, 255, 94);")
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(850, 95, 200, 40))
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.plainTextEdit_4.setFont(font)
        self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_5.setGeometry(QtCore.QRect(1080, 95, 31, 40))
        self.plainTextEdit_5.setStyleSheet("background-color: rgb(94, 255, 150);")
        self.plainTextEdit_5.setObjectName("plainTextEdit_5")
        self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_6.setGeometry(QtCore.QRect(1110, 95, 200, 40))
        self.plainTextEdit_6.setObjectName("plainTextEdit_6")
        self.plainTextEdit_6.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 130, MainWindow.width, MainWindow.height - 125))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(l)) # changed
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.setColumnWidth(0, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(1, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(2, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(3, int(MainWindow.width / 5) - 20)
        self.tableWidget.setColumnWidth(4, int(MainWindow.width / 5) - 20)
        self.retranslateUi(MainWindow, l, control_hazard_signals)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_memory_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() - 3)

    def show_register_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() - 2)

    def show_data_hazard(self):
        widgets.setCurrentIndex(widgets.currentIndex() - 1)

    def retranslateUi(self, MainWindow, l, control_hazard_signals):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Colors representing Control Hazard"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.data_hazard_button.setText(_translate("MainWindow", "Data Hazard"))
        self.control_hazard_button.setText(_translate("MainWindow", "Control Hazard"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Fetch"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Decode"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Execute"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Memory"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Write back"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Wrong Prediction"))
        self.plainTextEdit_4.setPlainText(_translate("MainWindow", "Came first time"))
        self.plainTextEdit_6.setPlainText(_translate("MainWindow", "Correct Prediction"))


        f = l
        for i in range(len(f)):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][0]))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][1]))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 2, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][2]))
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 3, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][3]))

            # adding colors for control_hazard
            if pipelining_enabled:
                if control_hazard_signals[i] == 1:
                    item.setBackground(QtGui.QColor(255, 94, 94))
                if control_hazard_signals[i] == 2:
                    item.setBackground(QtGui.QColor(247, 255, 94))
                if control_hazard_signals[i] == 3:
                    item.setBackground(QtGui.QColor(94, 255, 150))

            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 4, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][4]))

def display(l, control_hazard_signals, l_for):
    MainWindow2 = QtWidgets.QWidget()
    MainWindow3 = QtWidgets.QWidget()
    MainWindow4 = QtWidgets.QWidget()
    MainWindow5 = QtWidgets.QWidget()
    ui1 = display_data()
    ui1.setupUi(MainWindow2, "data_out.mc")
    ui2 = display_register()
    ui2.setupUi(MainWindow3, "reg_out.mc")
    ui3 = display_data_hazard()
    ui3.setupUi(MainWindow4, l_for)
    ui4 = display_control_hazard()
    ui4.setupUi(MainWindow5, l, control_hazard_signals)
    global widgets
    widgets = QtWidgets.QStackedWidget()
    widgets.setFixedHeight(970)
    widgets.setFixedWidth(1900)
    widgets.addWidget(MainWindow2)
    widgets.addWidget(MainWindow3)
    widgets.addWidget(MainWindow4)
    widgets.addWidget(MainWindow5)
    widgets.show()
    sys.exit(app.exec_())

def take_input():
    global app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow1 = QtWidgets.QMainWindow()
    ui1 = Ui_takeInput()
    ui1.setupUi(MainWindow1)
    MainWindow2 = QtWidgets.QMainWindow()
    ui2 = Ui_takeDataCacheInput()
    ui2.setupUi(MainWindow2)
    MainWindow3 = QtWidgets.QMainWindow()
    ui3 = Ui_takeInstructionCacheInput()
    ui3.setupUi(MainWindow3)
    global w
    w = QtWidgets.QStackedWidget()
    w.setFixedHeight(660)
    w.setFixedWidth(875)
    w.addWidget(MainWindow1)
    w.addWidget(MainWindow2)
    w.addWidget(MainWindow3)
    w.show()
    app.exec_()
    l = [data_cache_size, data_cache_block_size, data_cache_associativity, data_cache_ways, instruction_cache_size, instruction_cache_block_size, instruction_cache_associativity, instruction_cache_ways]
    return filename[0], pipelining_enabled, forwarding_enabled, print_registers_each_cycle, print_pipeline_registers, [print_specific_pipeline_registers, number], l
