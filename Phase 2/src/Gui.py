import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog
import time
import os

class Ui_takeInput(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(807, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(295, 270, 161, 61))
        self.pushButton.setObjectName("pushButton")

        global pipelining_enabled = False, forwarding_enabled = False, print_registers_each_cycle = False, print_specific_pipeline_registers = False, print_pipeline_registers = False
        self.pipelining_enabled = QtWidgets.QCheckBox(self.centralwidget)
        self.pipelining_enabled.setGeometry(QtCore.QRect(170, 120, 81, 20))
        self.pipelining_enabled.stateChanged.connect(lambda: pipelining_enabled = not pipelining_enabled)
          
        self.forwarding_enabled = QtWidgets.QCheckBox(self.centralwidget)
        self.forwarding_enabled.setGeometry(QtCore.QRect(170, 140, 81, 20))
        self.forwarding_enabled.stateChanged.connect(lambda: forwarding_enabled = not forwarding_enabled)
          
        self.print_registers_each_cycle = QtWidgets.QCheckBox(self.centralwidget)
        self.print_registers_each_cycle.setGeometry(QtCore.QRect(170, 160, 81, 20))
        self.print_registers_each_cycle.stateChanged.connect(lambda: print_registers_each_cycle = not print_registers_each_cycle)
          
        self.print_pipeline_registers = QtWidgets.QCheckBox(self.centralwidget)
        self.print_pipeline_registers.setGeometry(QtCore.QRect(170, 180, 81, 20))
        self.print_pipeline_registers.stateChanged.connect(lambda: print_pipeline_registers = not print_pipeline_registers)

        self.print_specific_pipeline_registers = QtWidgets.QCheckBox(self.centralwidget)
        self.print_specific_pipeline_registers.setGeometry(QtCore.QRect(170, 180, 81, 20))
        self.print_specific_pipeline_registers.stateChanged.connect(lambda: print_specific_pipeline_registers = not print_specific_pipeline_registers)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 180, 301, 41))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.pushButton.setText(_translate("MainWindow", "Choose File"))
        self.label.setText(_translate("MainWindow", "Choose the input file "))
        self.pushButton.clicked.connect(lambda: self.pushButton_handler(MainWindow))


    def openDialogBox(self, MainWindow):
        global filename
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, 'test')
        filename = QFileDialog.getOpenFileName(MainWindow, 'Open file', path, "*.mc")
        MainWindow.close()


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
        self.memory_button.setGeometry(QtCore.QRect(720, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(850, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.pipeline_button = QtWidgets.QPushButton(self.centralwidget)
        self.pipeline_button.setGeometry(QtCore.QRect(980, 3, 125, 40))
        self.pipeline_button.setObjectName("pipeline")
        self.register_button.clicked.connect(self.show_register_data)
        self.pipeline_button.clicked.connect(self.show_pipeline_data)
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

    def show_pipeline_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 2)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Memory Data"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.pipeline_button.setText(_translate("MainWindow", "Pipeline"))
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
        self.memory_button.setGeometry(QtCore.QRect(720, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(850, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.pipeline_button = QtWidgets.QPushButton(self.centralwidget)
        self.pipeline_button.setGeometry(QtCore.QRect(980, 3, 125, 40))
        self.pipeline_button.setObjectName("pipeline")
        self.memory_button.clicked.connect(self.show_memory_data)
        self.pipeline_button.clicked.connect(self.show_pipeline_data)
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
    
    def show_pipeline_data(self):
        widgets.setCurrentIndex(widgets.currentIndex() + 1)

    def retranslateUi(self, MainWindow, filename):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Register Data"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.pipeline_button.setText(_translate("MainWindow", "Pipeline"))
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


class display_pipeline(object):
    def setupUi(self, MainWindow, l):
        MainWindow.width = 1900
        MainWindow.height = 970
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, MainWindow.width, MainWindow.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(810, 50, 300, 35))
        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setGeometry(QtCore.QRect(720, 3, 125, 40))
        self.memory_button.setObjectName("memory")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(850, 3, 125, 40))
        self.register_button.setObjectName("register")
        self.pipeline_button = QtWidgets.QPushButton(self.centralwidget)
        self.pipeline_button.setGeometry(QtCore.QRect(980, 3, 125, 40))
        self.pipeline_button.setObjectName("pipeline")
        self.memory_button.clicked.connect(self.show_memory_data)
        self.register_button.clicked.connect(self.show_register_data)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 95, MainWindow.width, MainWindow.height - 100))
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

    def retranslateUi(self, MainWindow, l):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label.setText(_translate("MainWindow", "Pipeline at each Cycle"))
        self.memory_button.setText(_translate("MainWindow", "Data"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.pipeline_button.setText(_translate("MainWindow", "Pipeline"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Fetch"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Decode"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Execute"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Memory"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Write back"))

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
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 4, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(_translate("MainWindow", f[i][4]))

def display(l):
    MainWindow2 = QtWidgets.QWidget()
    MainWindow3 = QtWidgets.QWidget()
    MainWindow4 = QtWidgets.QWidget()
    ui1 = display_data()
    ui1.setupUi(MainWindow2, "data_out.mc")
    ui2 = display_register()
    ui2.setupUi(MainWindow3, "reg_out.mc")
    ui3 = display_pipeline()
    ui3.setupUi(MainWindow4, l)
    global widgets
    widgets = QtWidgets.QStackedWidget()
    widgets.setFixedHeight(970)
    widgets.setFixedWidth(1900)
    widgets.addWidget(MainWindow2)
    widgets.addWidget(MainWindow3)
    widgets.addWidget(MainWindow4)
    widgets.show()
    sys.exit(app.exec_())

def take_input():
    global app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_takeInput()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return filename[0], pipelining_enabled, forwarding_enabled, print_registers_each_cycle, print_specific_pipeline_registers, print_pipeline_registers

