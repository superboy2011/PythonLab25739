import sys
from PyQt5 import QtWidgets
from notelyLoginGUI import Ui_MainWindow
from notelyMainGUI import Ui_Logged_in_window


window_start = None
window_main = None


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.exit_btn.clicked.connect(lambda: sys.exit())
        self.signup_page_btn.clicked.connect(self.sign_up_form_load)

    def sign_up_form_load(self):
        global window_main
        window_main = StartWindow()
        window_main.show()
        self.hide()


class StartWindow(QtWidgets.QMainWindow, Ui_Logged_in_window):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Logged_in_window.__init__(self)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.go_bck_btn.clicked.connect(self.go_back_to_start_window)

    def go_back_to_start_window(self):
        window_start.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window_start = MyApp()
    window_start.show()
    sys.exit(app.exec_())
