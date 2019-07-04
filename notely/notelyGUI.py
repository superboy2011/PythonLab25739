import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDateTime, QRegExp
import PyQt5.QtGui
from PyQt5.QtWidgets import QMessageBox, QPushButton, QSizePolicy, QCheckBox

from notelyLoginGUI import Ui_MainWindow
from notelyMainGUI import Ui_Logged_in_window
import notelyConnection
from notelyClasses import NotelyNote, NotelyFolder
from functools import partial

window_start = None
window_main = None
button_folders = []
button_notes = []
chkbxs = []


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.exit_btn.clicked.connect(sys.exit)
        self.signup_page_btn.clicked.connect(self.sign_up_form_load)
        self.login_page_btn.clicked.connect(self.login_form_load)

    def sign_up_form_load(self):
        window_main.show()
        window_main.stackedWidget.setCurrentIndex(0)
        self.hide()

    def login_form_load(self):
        window_main.show()
        window_main.stackedWidget.setCurrentIndex(1)
        self.hide()


class StartWindow(QtWidgets.QMainWindow, Ui_Logged_in_window):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Logged_in_window.__init__(self)
        self.setupUi(self)
        self.back_btn.clicked.connect(self.go_back_to_start_window)
        self.back_btn_2.clicked.connect(self.go_back_to_start_window)
        self.sign_up_btn.clicked.connect(self.signup_user_gui)
        self.line_pass.returnPressed.connect(self.signup_user_gui)
        self.log_in_btn.clicked.connect(self.login_user_gui)
        self.line_pass_2.returnPressed.connect(self.login_user_gui)
        self.log_out_btn.clicked.connect(self.logout_user_gui)
        self.new_note_btn.clicked.connect(partial(self.add_note_page_render, "Uncategorized", 2))
        self.new_cat_btn.clicked.connect(partial(self.stackedWidget.setCurrentIndex, 5))
        self.go_bck_btn.clicked.connect(partial(self.stackedWidget.setCurrentIndex, 2))
        self.add_cat_btn.clicked.connect(self.add_folder_gui)
        self.new_cat_txt.returnPressed.connect(self.add_folder_gui)
        self.list_cat_btn.clicked.connect(self.show_all_folders_gui)
        self.gen_cat_btn.clicked.connect(partial(self.show_folder_contents_gui, "Uncategorized", 2))
        self.go_back_btn_3.clicked.connect(self.update_go_back_dis)
        self.delete_cat_btn.clicked.connect(self.delete_selected_folders_gui)
        self.go_back_btn_4.clicked.connect(self.delete_btn_bx_go_back_gui)
        self.no_commas = PyQt5.QtGui.QRegExpValidator(QRegExp("[^,]+"))
        self.line_note_name.setValidator(self.no_commas)
        self.line_note_name_2.setValidator(self.no_commas)
        self.new_cat_txt.setValidator(self.no_commas)

    def go_back_to_start_window(self):
        self.line_user.setText("")
        self.line_pass.setText("")
        self.line_first_name.setText("")
        self.line_last_name.setText("")
        self.line_email.setText("")
        self.line_user_2.setText("")
        self.line_pass_2.setText("")
        window_start.show()
        self.hide()

    def signup_user_gui(self):
        username = self.line_user.text()
        password = self.line_pass.text()
        first_name = self.line_first_name.text()
        last_name = self.line_last_name.text()
        email = self.line_email.text()
        success, result, code = notelyConnection.signup_user(username, password, email, first_name, last_name)
        if success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("You Successfully signed up")
            msg.setWindowTitle("Result")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.line_user.setText("")
            self.line_pass.setText("")
            self.line_first_name.setText("")
            self.line_last_name.setText("")
            self.line_email.setText("")
            self.go_back_to_start_window()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error while signing up")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msg.exec()
            if return_value == QMessageBox.Cancel:
                self.line_user.setText("")
                self.line_pass.setText("")
                self.line_first_name.setText("")
                self.line_last_name.setText("")
                self.line_email.setText("")
                self.go_back_to_start_window()

    def login_user_gui(self):
        username = self.line_user_2.text()
        password = self.line_pass_2.text()
        success, result, code = notelyConnection.login_user(username, password)
        if success:
            self.line_user_2.setText("")
            self.line_pass_2.setText("")
            self.stackedWidget.setCurrentIndex(2)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error while logging in")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msg.exec()
            if return_value == QMessageBox.Cancel:
                self.line_user_2.setText("")
                self.line_pass_2.setText("")
                self.go_back_to_start_window()

    def logout_user_gui(self):
        notelyConnection.logout_user()
        self.hide()
        window_start.show()

    def add_note_page_render(self, category, prev_page_index):
        self.stackedWidget.setCurrentIndex(3)
        self.cat_note_lbl.setText(("Category: " + category))
        self.discard_note_btn.clicked.connect(partial(self.discard_note_go_back_dis, prev_page_index))
        self.save_note_btn.clicked.connect(partial(self.add_note_gui, category, prev_page_index))

    def discard_note_go_back_dis(self, prev_page_index):
        self.discard_note_btn.disconnect()
        self.save_note_btn.disconnect()
        self.stackedWidget.setCurrentIndex(prev_page_index)

    def add_note_gui(self, category, prev_page_index):
        if self.reminder_chkbx.isChecked():
            new_note = NotelyNote(self.line_note_name.text(), category, self.note_data_txt.toPlainText(),
                                  self.reminder_dt.dateTime().toPyDateTime())
        else:
            new_note = NotelyNote(self.line_note_name.text(), category, self.note_data_txt.toPlainText())
        success, result, code = notelyConnection.add_note_user(new_note)
        if success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("Note added successfully")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.discard_note_btn.disconnect()
            self.save_note_btn.disconnect()
            self.line_note_name.setText("")
            self.note_data_txt.setText("")
            if prev_page_index == 2:
                self.stackedWidget.setCurrentIndex(2)
            elif prev_page_index == 6:
                self.come_back_to_show_folder(category)
            else:
                print('FATAL ERROR IN ADD NOTE REDIRECT')
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error while adding note")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msg.exec()
            if return_value == QMessageBox.Cancel:
                self.discard_note_btn.disconnect()
                self.save_note_btn.disconnect()
                self.line_note_name.setText("")
                self.note_data_txt.setText("")
                self.stackedWidget.setCurrentIndex(prev_page_index)

    def add_folder_gui(self):
        new_folder = NotelyFolder(self.new_cat_txt.text(), [])
        success, result, code = notelyConnection.add_folder_user(new_folder)
        if success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("Folder added successfully")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.new_cat_txt.setText("")
            self.stackedWidget.setCurrentIndex(2)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error while adding folder")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msg.exec()
            if return_value == QMessageBox.Cancel:
                self.new_cat_txt.setText("")
                self.stackedWidget.setCurrentIndex(2)

    def show_all_folders_gui(self):
        success, result, code = notelyConnection.get_folder_list_user()
        if not success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error while loading category list")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec()
        else:
            self.stackedWidget.setCurrentIndex(7)
            global button_folders, chkbxs
            button_folders = []  # x: 60, y_start: 20, height:35, width: 200
            chkbxs = []  # X:20, y_start:20, height:35, width: 20
            for idx, category in enumerate(result):
                btn = QPushButton(self.scrollArea_2)
                btn.setText(category)
                btn.setGeometry(QtCore.QRect(60, 20 + 55 * idx, 200, 35))
                btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                btn.setObjectName(("btn_cat" + str(idx)))
                btn.show()
                btn.clicked.connect(partial(self.show_folder_contents_gui, category, 7))
                button_folders.append((btn, category))
                chkbx = QCheckBox(self.scrollAreaWidgetContents_2)
                chkbx.setText("")
                chkbx.setGeometry(QtCore.QRect(20, 20 + 55 * idx, 20, 35))
                chkbx.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                chkbx.setObjectName(("chkbx_cat_" + str(idx)))
                chkbx.show()
                chkbxs.append((chkbx, category))

    def delete_selected_folders_gui(self):
        global button_folders, chkbxs
        checked = False
        for chkbx in chkbxs:
            if chkbx[0].isChecked():
                checked = True
        if not checked:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("No folder selected")
            msg.setWindowTitle("No Selection")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        else:
            for btn in button_folders:
                btn[0].deleteLater()
            button_folders = []
            for chkbx in chkbxs:
                if chkbx[0].isChecked():
                    notelyConnection.delete_folder_user(chkbx[1])
                chkbx[0].deleteLater()
            chkbxs = []
            self.show_all_folders_gui()

    def delete_btn_bx_go_back_gui(self):
        global button_folders, chkbxs
        for btn in button_folders:
            btn[0].deleteLater()
        button_folders = []
        for ckbx in chkbxs:
            ckbx[0].deleteLater()
        chkbxs = []
        self.stackedWidget.setCurrentIndex(2)

    def come_back_to_show_folder(self, category):
        global button_notes
        for btn in button_notes:
            btn[0].deleteLater()
        button_notes = []
        self.new_note_cat_btn.disconnect()
        self.go_back_btn_2.disconnect()
        if category == 'Uncategorized':
            prev_page_index = 2
        else:
            prev_page_index = 7
        self.show_folder_contents_gui(category, prev_page_index)

    def show_folder_contents_gui(self, category, prev_page_index):
        success, result, code = notelyConnection.get_folder_content_user(category)
        if not success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error while loading category content")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec()
        else:
            result = result.list_notes
            self.stackedWidget.setCurrentIndex(6)
            self.cat_name_lbl.setText(category)
            global button_notes
            button_notes = []  # x: 20, y_start: 20, height:35, width: 240
            for idx, note_name in enumerate(result):
                btn = QPushButton(self.scrollArea)
                btn.setText(note_name)
                btn.setGeometry(QtCore.QRect(60, 20 + 55 * idx, 200, 35))
                btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                btn.setObjectName(("btn_cat" + str(idx)))
                btn.show()
                btn.clicked.connect(partial(self.update_page_render_gui, note_name, category, btn, prev_page_index))
                button_notes.append((btn, category))
            self.new_note_cat_btn.clicked.connect(partial(self.add_note_page_render, category, 6))
            self.go_back_btn_2.clicked.connect(partial(self.delete_btn_go_back_gui, prev_page_index))

    def update_page_render_gui(self, note_name, category, btn, prev_page_index):
        success, result, code = notelyConnection.get_note_user(note_name, category)
        if not success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error while loading note")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec()
        else:
            self.line_note_name_2.setText(result.name)
            self.cat_note_lbl_2.setText("Category: " + category)
            self.note_data_txt_2.setText(result.data)
            if result.reminder.year != 1:
                self.reminder_chkbx_2.setChecked(True)
                self.reminder_dt_2.setDateTime(QDateTime.fromString(result.reminder.strftime("%Y %m %d H %M %S"),
                                                                    'yyyy MM dd hh mm ss'))
            else:
                self.reminder_chkbx_2.setChecked(False)
            self.updat_note_btn.clicked.connect(partial(self.update_note_gui, result, btn, prev_page_index))
            self.delete_note_btn.clicked.connect(partial(self.delete_note_gui, note_name, category, prev_page_index))
            self.stackedWidget.setCurrentIndex(4)

    def update_go_back_dis(self):
        self.updat_note_btn.disconnect()
        self.delete_note_btn.disconnect()
        self.stackedWidget.setCurrentIndex(6)

    def update_note_gui(self, old_note, btn, prev_page_index):
        if self.reminder_chkbx_2.isChecked():
            new_note = NotelyNote(self.line_note_name_2.text(), old_note.folder_name, self.note_data_txt_2.text(),
                                  self.reminder_dt_2.dateTime().toPyDateTime())
        else:
            new_note = NotelyNote(self.line_note_name_2.text(), old_note.folder_name, self.note_data_txt_2.text())
        success, result, code = notelyConnection.update_note_user(new_note, old_note)
        if success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("Note updated successfully")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.updat_note_btn.disconnect()
            self.delete_note_btn.disconnect()
            btn.setText(self.line_note_name_2.text())
            btn.disconnect()
            btn.clicked.connect(partial(self.update_page_render_gui, self.line_note_name_2.text(), old_note.folder_name,
                                        btn, prev_page_index))
            self.stackedWidget.setCurrentIndex(6)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error while updating note")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msg.exec()
            if return_value == QMessageBox.Cancel:
                self.updat_note_btn.disconnect()
                self.delete_note_btn.disconnect()
                self.stackedWidget.setCurrentIndex(7)

    def delete_note_gui(self, note_name, category, prev_page_index):
        success, result, code = notelyConnection.delete_note_user(note_name, category)
        if success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("Note deleted successfully")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            global button_notes
            for btn in button_notes:
                btn[0].deleteLater()
            button_notes = []
            self.new_note_cat_btn.disconnect()
            self.go_back_btn_2.disconnect()
            self.updat_note_btn.disconnect()
            self.delete_note_btn.disconnect()
            self.show_folder_contents_gui(category, prev_page_index)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error while updating note")
            msg.setInformativeText(result)
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msg.exec()
            if return_value == QMessageBox.Cancel:
                self.updat_note_btn.disconnect()
                self.delete_note_btn.disconnect()
                self.stackedWidget.setCurrentIndex(7)

    def delete_btn_go_back_gui(self, prev_page_index):
        global button_notes
        for btn in button_notes:
            btn[0].deleteLater()
        button_notes = []
        self.new_note_cat_btn.disconnect()
        self.go_back_btn_2.disconnect()
        self.stackedWidget.setCurrentIndex(prev_page_index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    notelyConnection.initialize()
    window_start = MyApp()
    window_main = StartWindow()
    window_start.show()
    sys.exit(app.exec_())
