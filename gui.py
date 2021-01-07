

import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import select
import sys
import argparse
from threading import Thread
import json
from signal import signal, SIGUSR1, SIGUSR2
from os import kill, getpid, execlp
import os

BUFFER_SIZE = 2048
ip = "linux8.csie.org"
port = 1487
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buf = ""

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.username = 0
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(524, 355)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(200, 280, 200, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.usernamelineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.usernamelineEdit.setGeometry(QtCore.QRect(130, 280, 60, 20))
        self.usernamelineEdit.setObjectName("usernamelineEdit")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(130, 240, 121, 21))
        self.label1.setObjectName("label1")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(410, 280, 75, 23))
        self.sendButton.setObjectName("sendButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 220, 121, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 200, 121, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(130, 180, 121, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 160, 121, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(130, 140, 121, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 120, 121, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(130, 100, 121, 21))
        self.label_8.setObjectName("label_8")
        self.reloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.reloadButton.setGeometry(QtCore.QRect(40, 280, 75, 23))
        self.reloadButton.setObjectName("reloadButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 524, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sendButton.clicked.connect(self.presssend)
        self.reloadButton.clicked.connect(self.pressreload)
        
    
    def pressreload(self):
        # self.data = sock.recv(self.BUFFER_SIZE)
        _translate = QtCore.QCoreApplication.translate
        # if not self.data:
        #     self.label1.setText(_translate("MainWindow", "Connection Broken\033[0m"))
        #D = self.data.decode()
        #self.label1.setText(_translate("MainWindow", f"D"))
        pid = os.fork()
        if pid == 0:
            execlp("/usr/bin/python3", "python3",  "predict_str.py")
        else:
            fd = os.open("tmp", os.O_RDWR, 0o755)
            nret = os.read(fd, 1024)
            print(nret.decode("utf-8"))
        


    def presssend(self):
        global buf
        self.data = self.lineEdit.text()
        _translates = QtCore.QCoreApplication.translate
        self.lineEdit.setText(_translates("MainWindow", ""))
        print(f"when clicked: {self.data}")
        if not self.username:
            self.username = self.data
            buf = self.data
            kill(getpid(), SIGUSR1)
        else:
            to = self.usernamelineEdit.text()
            self.label1.setText(_translates("MainWindow",f"{self.data}"))
            to_send = {"type": "string", "to" : to, "body": self.data}
            if to_send["type"] == "string":
                to_send = json.dumps(to_send)
                buf = to_send
                print(f"buf: {buf}")
                kill(getpid(), SIGUSR1)

    def send_file(self,filename):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, 1689))
        self.s.send(filename.encode("utf-8"))
        with open(filename, "rb") as f:
            self.bytedata = f.read(4096)
            while self.bytedata:
                self.s.send(bytedata)
                self.bytedata = f.read(4096)
        self.s.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "TextLabel"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.reloadButton.setText(_translate("MainWindow", "Reload"))


def recv_msg(sock):
    while True:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            print("Connection Broken\033[0m")
            break
        print(data.decode())

def showgui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def socket_thread():
    client.connect((ip, port))
    print("Connected")
    while True:
        msg = client.recv(4096)
        print(msg.decode("utf-8"))

def send_to_server(signum, _):
    print("SIGUSR1 caught")
    client.send(buf.encode("utf-8"))
    print(f"sent {buf}")

def main():
    signal(SIGUSR1, send_to_server)
    socket_t = Thread(target=socket_thread)
    socket_t.start()
    showgui()

if __name__ == "__main__":
    main()