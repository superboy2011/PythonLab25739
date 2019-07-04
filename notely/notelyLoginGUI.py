# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notelyLoginGUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import rsc1


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(626, 417)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 626, 417))
        self.graphicsView.setStyleSheet("background-image: url(:/newPrefix/notebook-wood-table-background_38045-567.jpg);")
        self.graphicsView.setObjectName("graphicsView")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(420, 90, 151, 241))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(70)
        self.splitter.setObjectName("splitter")
        self.login_page_btn = QtWidgets.QPushButton(self.splitter)
        self.login_page_btn.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.login_page_btn.setObjectName("login_page_btn")
        self.signup_page_btn = QtWidgets.QPushButton(self.splitter)
        self.signup_page_btn.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"")
        self.signup_page_btn.setObjectName("signup_page_btn")
        self.exit_btn = QtWidgets.QPushButton(self.splitter)
        self.exit_btn.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.exit_btn.setIconSize(QtCore.QSize(16, 16))
        self.exit_btn.setObjectName("exit_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NoteLY"))
        self.login_page_btn.setText(_translate("MainWindow", "Login"))
        self.signup_page_btn.setText(_translate("MainWindow", "Sign up"))
        self.exit_btn.setText(_translate("MainWindow", "Exit"))
