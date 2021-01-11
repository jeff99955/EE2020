import sys
import socket
from threading import Thread
import json
from signal import SIGKILL
from os import kill, getpid, execlp, mkfifo, fork, wait, remove
import os
from atexit import register
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5 import uic


BUFFER_SIZE = 2048
ip = "linux8.csie.org"
port = 1487
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buf = ""
username = ""
path_to_python3 = "/usr/bin/python3"
user_addr = {}


def run_AI():
    pid = fork()
    if pid == 0:
        execlp(path_to_python3, "python3",  "predict_str.py")
    else:
        print("this will be executed")
        fd = os.open("tmp", os.O_RDWR, 0o755)
        nret = os.read(fd, 1024)
        nret = nret.decode("utf-8")
        print(nret)
        return nret


def send(st: str):
    client.send(st.encode("utf-8"))

    print(f"sent {buf}")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global username
        self.username = username
        print("in main window: username", username)

        self.mdict = {}
        for i in range(1, 26):
            self.mdict[i] = " "
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 518)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(193, 193, 193))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 43, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 43, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(193, 193, 193))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 43, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 43, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 43, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 43, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet("background-color:rgb(0, 43, 54)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setKerning(True)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setAutoFillBackground(False)
        self.lineEdit_2.setStyleSheet("font: 10pt \"Microsoft New Tai Lue\";\n"
                                      "\n"
                                      "background-color:rgb(0, 17, 22);\n"
                                      "border:rgb(85, 255, 255);\n"
                                      "color:rgb(200, 200, 200)")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgb(0,17,22);\n"
                                    "border:rgb(0, 43, 54);\n"
                                    "color:rgb(200,200,200)\n"
                                    "")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.messageButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.messageButton.setFont(font)
        self.messageButton.setStyleSheet("background-color: rgb(42, 161, 152); color: rgb(255, 255, 255)\n"
                                         "")
        self.messageButton.setObjectName("messageButton")
        self.gridLayout.addWidget(self.messageButton, 1, 3, 1, 1)
        self.fileButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(10)
        self.fileButton.setFont(font)
        self.fileButton.setStyleSheet("background-color: rgb(42, 161, 152); color: rgb(255, 255, 255)\n"
                                      "")
        self.fileButton.setObjectName("fileButton")
        self.gridLayout.addWidget(self.fileButton, 1, 6, 1, 1)
        self.imageButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(10)
        self.imageButton.setFont(font)
        self.imageButton.setStyleSheet("background-color: rgb(42, 161, 152); color: rgb(255, 255, 255)\n"
                                       "")
        self.imageButton.setObjectName("imageButton")
        self.gridLayout.addWidget(self.imageButton, 1, 5, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.AlternateBase, brush)
        self.scrollArea.setPalette(palette)
        self.scrollArea.setStyleSheet("border:rgb(0, 43, 54);\n"
                                      "selection-color: rgb(85, 255, 255);\n"
                                      "background-color:transparent;\n"
                                      "gridline-color: rgb(85, 255, 255);\n"
                                      "alternate-background-color: rgb(85, 255, 255);\n"
                                      "")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 516, 502))
        self.scrollAreaWidgetContents.setStyleSheet("border:none")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(10)
        font.setKerning(True)
        self.groupBox.setFont(font)
        self.groupBox.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setStyleSheet("border:none")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")

        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setFont(font)
        self.label.setStyleSheet("\n"
                                 "color: rgb(234, 234, 234);")
        self.label.setObjectName("label")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.SpanningRole, self.label)

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.SpanningRole, self.label_2)

        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_3.setObjectName("label")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.SpanningRole, self.label_3)

        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_4.setObjectName("label")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.SpanningRole, self.label_4)

        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_5.setObjectName("label")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.SpanningRole, self.label_5)

        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_6.setObjectName("label")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.SpanningRole, self.label_6)

        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_7.setObjectName("label")
        self.formLayout.setWidget(
            6, QtWidgets.QFormLayout.SpanningRole, self.label_7)

        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_8.setObjectName("label")
        self.formLayout.setWidget(
            7, QtWidgets.QFormLayout.SpanningRole, self.label_8)

        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("\n"
                                   "color: rgb(234, 234, 234);")
        self.label_9.setObjectName("label")
        self.formLayout.setWidget(
            8, QtWidgets.QFormLayout.SpanningRole, self.label_9)

        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_10.setObjectName("label")
        self.formLayout.setWidget(
            9, QtWidgets.QFormLayout.SpanningRole, self.label_10)

        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_11.setObjectName("label")
        self.formLayout.setWidget(
            10, QtWidgets.QFormLayout.SpanningRole, self.label_11)

        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_12.setObjectName("label")
        self.formLayout.setWidget(
            11, QtWidgets.QFormLayout.SpanningRole, self.label_12)

        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_13.setObjectName("label")
        self.formLayout.setWidget(
            12, QtWidgets.QFormLayout.SpanningRole, self.label_13)

        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_14.setObjectName("label")
        self.formLayout.setWidget(
            13, QtWidgets.QFormLayout.SpanningRole, self.label_14)

        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_15.setObjectName("label")
        self.formLayout.setWidget(
            14, QtWidgets.QFormLayout.SpanningRole, self.label_15)

        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_16.setObjectName("label")
        self.formLayout.setWidget(
            15, QtWidgets.QFormLayout.SpanningRole, self.label_16)

        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_17.setObjectName("label")
        self.formLayout.setWidget(
            16, QtWidgets.QFormLayout.SpanningRole, self.label_17)

        self.label_18 = QtWidgets.QLabel(self.groupBox)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_18.setObjectName("label")
        self.formLayout.setWidget(
            17, QtWidgets.QFormLayout.SpanningRole, self.label_18)

        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_19.setObjectName("label")
        self.formLayout.setWidget(
            18, QtWidgets.QFormLayout.SpanningRole, self.label_19)

        self.label_20 = QtWidgets.QLabel(self.groupBox)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_20.setObjectName("label")
        self.formLayout.setWidget(
            19, QtWidgets.QFormLayout.SpanningRole, self.label_20)

        self.label_21 = QtWidgets.QLabel(self.groupBox)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_21.setObjectName("label")
        self.formLayout.setWidget(
            20, QtWidgets.QFormLayout.SpanningRole, self.label_21)

        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_22.setObjectName("label")
        self.formLayout.setWidget(
            21, QtWidgets.QFormLayout.SpanningRole, self.label_22)

        self.label_23 = QtWidgets.QLabel(self.groupBox)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_23.setObjectName("label")
        self.formLayout.setWidget(
            22, QtWidgets.QFormLayout.SpanningRole, self.label_23)

        self.label_24 = QtWidgets.QLabel(self.groupBox)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_24.setObjectName("label")
        self.formLayout.setWidget(
            23, QtWidgets.QFormLayout.SpanningRole, self.label_24)

        self.label_25 = QtWidgets.QLabel(self.groupBox)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("\n"
                                    "color: rgb(234, 234, 234);")
        self.label_25.setObjectName("label")
        self.formLayout.setWidget(
            24, QtWidgets.QFormLayout.SpanningRole, self.label_25)

        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 7)
        self.AIButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.AIButton.setFont(font)
        self.AIButton.setStyleSheet("background-color: rgb(42, 161, 152); color: rgb(255, 255, 255)\n"
                                    "")
        self.AIButton.setObjectName("AIButton")
        self.gridLayout.addWidget(self.AIButton, 1, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 551, 22))
        self.menubar.setObjectName("menubar")
        self.menuAI = QtWidgets.QMenu(self.menubar)
        self.menuAI.setObjectName("menuAI")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAI.menuAction())

        self.retranslateUi(MainWindow)


# file button
        self.fileButton.clicked.connect(self.filebuttonclicked)
# file button

        # now it only connects with the function printing f"Hi, {self.username} !"
        # it will also be used to receive messages

        self.messageButton.clicked.connect(self.passmessages)
        # self.messageButton.clicked.connect()
        # will get the username of the person you want to chat with from lineEdit2

        self.AIButton.clicked.connect(self.AIclicked)
        # will be connected with the gesture recognizing program

        self.imageButton.clicked.connect(self.imagebuttonclicked)
        # will be connected with a image sending function

    def AIclicked(self):
        msg = run_AI()
        self.lineEdit.setText(msg)
        self.passmessages()

    def imagebuttonclicked(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            MainWindow, "QFileDialog,getOpenFileName()", "", "All Files (*)", options=options)
        to = self.lineEdit_2.text()
        if not to or not fileName:
            return
        to_send = {"type": "file", "to": to,
                   "body": "./" + fileName.split('/')[-1]}
        to_ip = user_addr[to_send["to"]]
        filename = to_send["body"]
        to_send = json.dumps(to_send)
        client.send(to_send.encode("utf-8"))
        pid = fork()
        if pid == 0:
            print(to_ip, filename)
            execlp("./client", "./client", to_ip, filename)
        status = wait()
        if status[1]:
            print("Error", "Cannot send the file")
        else:
            print("Success", "Succeed in sending files")

    def filebuttonclicked(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            MainWindow, "QFileDialog,getOpenFileName()", "", "All Files (*)", options=options)
        print(fileName)
        to = self.lineEdit_2.text()
        to_send = {"type": "file", "to": to,
                   "body": "./" + fileName.split('/')[-1]}
        to_ip = user_addr[to_send["to"]]
        filename = to_send["body"]
        to_send = json.dumps(to_send)
        client.send(to_send.encode("utf-8"))
        pid = fork()
        if pid == 0:
            print(to_ip, filename)
            execlp("./client", "./client", to_ip, filename)
        status = wait()
        if status[1]:
            self.show("Error", "Cannot send the file")
        else:
            self.show("Success", "Succeed in sending files")

    def show(self, type: str, text: str):
        QMessageBox.about(self, type, text)

    def passmessages(self):
        _translates = QtCore.QCoreApplication.translate
        self.input = self.lineEdit.text()
        self.lineEdit.setText(_translates("MainWindow", ""))

        for i in range(1, 25):
            self.mdict[i] = self.mdict[i+1]
        self.mdict[25] = "Me: " + self.input
        # print(self.mdict)
        self.label_25.setText(_translates("MainWindow", f"{self.mdict[25]}"))
        self.label_24.setText(_translates("MainWindow", f"{self.mdict[24]}"))
        self.label_23.setText(_translates("MainWindow", f"{self.mdict[23]}"))
        self.label_22.setText(_translates("MainWindow", f"{self.mdict[22]}"))
        self.label_21.setText(_translates("MainWindow", f"{self.mdict[21]}"))
        self.label_20.setText(_translates("MainWindow", f"{self.mdict[20]}"))
        self.label_19.setText(_translates("MainWindow", f"{self.mdict[19]}"))
        self.label_18.setText(_translates("MainWindow", f"{self.mdict[18]}"))
        self.label_17.setText(_translates("MainWindow", f"{self.mdict[17]}"))
        self.label_16.setText(_translates("MainWindow", f"{self.mdict[16]}"))
        self.label_15.setText(_translates("MainWindow", f"{self.mdict[15]}"))
        self.label_14.setText(_translates("MainWindow", f"{self.mdict[14]}"))
        self.label_13.setText(_translates("MainWindow", f"{self.mdict[13]}"))
        self.label_12.setText(_translates("MainWindow", f"{self.mdict[12]}"))
        self.label_11.setText(_translates("MainWindow", f"{self.mdict[11]}"))
        self.label_10.setText(_translates("MainWindow", f"{self.mdict[10]}"))
        self.label_9.setText(_translates("MainWindow", f"{self.mdict[9]}"))
        self.label_8.setText(_translates("MainWindow", f"{self.mdict[8]}"))
        self.label_7.setText(_translates("MainWindow", f"{self.mdict[7]}"))
        self.label_6.setText(_translates("MainWindow", f"{self.mdict[6]}"))
        self.label_5.setText(_translates("MainWindow", f"{self.mdict[5]}"))
        self.label_4.setText(_translates("MainWindow", f"{self.mdict[4]}"))
        self.label_3.setText(_translates("MainWindow", f"{self.mdict[3]}"))
        self.label_2.setText(_translates("MainWindow", f"{self.mdict[2]}"))
        self.label.setText(_translates("MainWindow", f"{self.mdict[1]}"))
        to = self.lineEdit_2.text()
        to_send = {"type": "string", "to": to, "body": self.input}
        to_send = json.dumps(to_send)
        send(to_send)

    def reloadmessage(self):
        global buf
        for i in range(1, 25):
            self.mdict[i] = self.mdict[i+1]
        self.mdict[25] = buf
        # print(self.mdict)
        self.label_25.setText(self.mdict[25])
        self.label_24.setText(self.mdict[24])
        self.label_23.setText(self.mdict[23])
        self.label_22.setText(self.mdict[22])
        self.label_21.setText(self.mdict[21])
        self.label_20.setText(self.mdict[20])
        self.label_19.setText(self.mdict[19])
        self.label_18.setText(self.mdict[18])
        self.label_17.setText(self.mdict[17])
        self.label_16.setText(self.mdict[16])
        self.label_15.setText(self.mdict[15])
        self.label_14.setText(self.mdict[14])
        self.label_13.setText(self.mdict[13])
        self.label_12.setText(self.mdict[12])
        self.label_11.setText(self.mdict[11])
        self.label_10.setText(self.mdict[10])
        self.label_9.setText(self.mdict[9])
        self.label_8.setText(self.mdict[8])
        self.label_7.setText(self.mdict[7])
        self.label_6.setText(self.mdict[6])
        self.label_5.setText(self.mdict[5])
        self.label_4.setText(self.mdict[4])
        self.label_3.setText(self.mdict[3])
        self.label_2.setText(self.mdict[2])
        self.label.setText(self.mdict[1])

    def retranslateUi(self, MainWindow):
        global username
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", ""))
        self.messageButton.setText(_translate("MainWindow", "Send"))
        self.fileButton.setText(_translate("MainWindow", "File"))
        self.imageButton.setText(_translate("MainWindow", "Image"))
        self.label_2.setText(_translate("MainWindow", " "))
        self.label_3.setText(_translate("MainWindow", " "))
        self.label_4.setText(_translate("MainWindow", " "))
        self.label_5.setText(_translate("MainWindow", " "))
        self.label_6.setText(_translate("MainWindow", " "))
        self.label_7.setText(_translate("MainWindow", " "))
        self.label_8.setText(_translate("MainWindow", " "))
        self.label_9.setText(_translate("MainWindow", " "))
        self.label_10.setText(_translate("MainWindow", " "))
        self.label_11.setText(_translate("MainWindow", " "))
        self.label_12.setText(_translate("MainWindow", " "))
        self.label_13.setText(_translate("MainWindow", " "))
        self.label_14.setText(_translate("MainWindow", " "))
        self.label_15.setText(_translate("MainWindow", " "))
        self.label_16.setText(_translate("MainWindow", " "))
        self.label_17.setText(_translate("MainWindow", " "))
        self.label_18.setText(_translate("MainWindow", " "))
        self.label_19.setText(_translate("MainWindow", " "))
        self.label_20.setText(_translate("MainWindow", " "))
        self.label_21.setText(_translate("MainWindow", " "))
        self.label_22.setText(_translate("MainWindow", " "))
        self.label_23.setText(_translate("MainWindow", " "))
        self.label_24.setText(_translate("MainWindow", " "))
        self.label_25.setText(_translate("MainWindow", " "))
        self.label.setText(_translate("MainWindow", " "))
        self.AIButton.setText(_translate("MainWindow", "AI"))
        self.menuAI.setTitle(_translate("MainWindow", " "))


class Ui_Dialog(object):
    def setupUi(self, Dialog, direct):
        Dialog.setObjectName("Dialog")
        Dialog.resize(179, 112)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.retranslateUi(Dialog)

        self.buttonBox.accepted.connect(self.setusername)
        # when accepted, set username
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(self.close)
        # when rejected, close the whole program
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.direct = direct

    def setusername(self):
        global username
        username = self.lineEdit.text()
        print(username)
        send(username)
        self.direct.show()

    def close(self):
        sys.exit()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Username:"))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
uui = Ui_MainWindow()
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()


def showgui():
    global username
    global app, MainWindow, uui, Dialog, ui
    uui.setupUi(MainWindow)
    ui.setupUi(Dialog, MainWindow)
    Dialog.show()
    # MainWindow.show()
    sys.exit(app.exec_())


def socket_thread():
    global buf
    client.connect((ip, port))
    print("Connected")
    while True:
        msg = client.recv(4096)
        if not msg:
            kill(getpid(), SIGKILL)
        try:
            mj = json.loads(msg)
            print("original message:", mj)
            if mj["type"] == "string" or mj["type"] == "message":
                buf = mj["from"] + ": " + mj["body"]
                uui.reloadmessage()
            elif mj["type"] == "file":
                buf = "Receiving file from " + \
                    mj["to"] + ", saving to " + mj["body"]
                pid = fork()
                if pid == 0:
                    execlp("./server", "./server")
                status = wait()
                print("server returned", status[0])
                uui.reloadmessage()
            elif mj["type"] == "image":
                buf = "Receiving image from " + \
                    mj["to"] + ", saving to " + mj["body"]
                uui.reloadmessage()
            elif mj["type"] == "setting":
                i = mj["set"]
                if i:
                    config = mj["body"]
                    for u in config:
                        user_addr[u] = config[u]
                    print("user_addr=>", user_addr)
                else:
                    user = mj["user"]
                    del user_addr[user]
        except ValueError:
            print(msg.decode("utf-8"))
        except KeyError as e:
            print("KeyError", e)


def ae():
    remove("tmp")


def main():
    register(ae)
    mkfifo("tmp", 0o755)
    socket_t = Thread(target=socket_thread)
    socket_t.start()
    showgui()


if __name__ == "__main__":
    main()