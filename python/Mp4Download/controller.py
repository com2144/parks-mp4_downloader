#!/usr/bin/env python
# :coding: utf-8

from model import DownLoadModel
from view import DownLoadMainView
from view import BrowseDialog
from PySide2.QtWidgets import *
import sys
from shotgun_api3 import Shotgun


class DownLoadController:
    def __init__(self, main_window):
        model = DownLoadModel()
        self.main_window = main_window
        self.view = DownLoadMainView()

        self.dialog = None

        self.path = model.path

        self.browse_sig = False

        self.main_ui()

    def main_ui(self):
        self.view.path_line_edit.setPlaceholderText("Select the save folder")

        self.view.path_hbox_layout.addWidget(self.view.path_line_edit)
        self.view.path_hbox_layout.addWidget(self.view.browse_button)
        self.view.main_vbox_layout.addLayout(self.view.path_hbox_layout)

        self.view.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.view.user_controller_btn_hbox_layout.addWidget(self.view.ok_button)
        self.view.user_controller_btn_hbox_layout.addWidget(self.view.cancel_button)
        self.view.main_vbox_layout.addLayout(self.view.user_controller_btn_hbox_layout)

        self.view.ok_button.clicked.connect(self.on_ok_button_clicked)
        self.view.cancel_button.clicked.connect(self.on_cancel_button_clicked)

        self.view.setLayout(self.view.main_vbox_layout)
    def on_browse_button_clicked(self):
        self.browse_sig = True

        if self.dialog is not None:
            self.dialog.close()

        browse_option = BrowseDialog()
        self.path = browse_option.option

        if not self.path:
            self.show_warning('Choose the directory')
        else:
            self.view.path_line_edit.setText(self.path)

    def on_ok_button_clicked(self):
        self.show_warning('Mp4 file save!')
        self.browse_sig = False

    def on_cancel_button_clicked(self):
        self.main_window.close()

    @staticmethod
    def show_warning(error_message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(f"{error_message}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    controller = DownLoadController(window)
    window.setCentralWidget(controller.view)
    window.setWindowTitle('Mp4 Downloader')
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# def main():
#     app = QApplication()
#     window = QMainWindow()
#     controller = DownLoadController(window)
#     window.setCentralWidget(controller.view)
#     window.setWindowTitle('Mp4 Downloader')
#     window.show()
#     app.exec_()
#
# if __name__ == '__main__':
#     main()
