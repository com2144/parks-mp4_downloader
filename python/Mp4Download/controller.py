# !/usr/bin/env python
# :coding: utf-8

from model import DownLoadModel
from view import *
from action_handler import *
from PySide2.QtWidgets import *
import sys
import os


class DownLoadController:
    def __init__(self, main_window, argv):

        self.action = ActionHandler(argv)

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
        self.download_url_file()
        if os.path.exists(self.path):
            self.show_warning('Mp4 files save!')
        else:
            self.show_warning('Failed to save Mp4 files')
        self.browse_sig = False

    def on_cancel_button_clicked(self):
        self.browse_sig = False
        self.main_window.close()

    @staticmethod
    def show_warning(error_message):
        warning_box_style = """
            QMessageBox{
                font: 15pt "Courier New";
                background-color: rgb(50, 50, 50);
                color: rgb(225, 225, 225);
            }

            /* Set the style of the text label */
            QLabel {
                color: rgb(225, 225, 225);
                font-size: 18px;
            }

            /* Set the style of the OK button */
            QPushButton {
                background-color: rgb(40, 40, 40);
                color: rgb(225, 225, 225);
                padding: 5px;
                border: 1px solid rgb(225, 225, 225);
                border-radius: 3px;
            }

            /* Set the style of the OK button when hovered */
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }

            /* Set the style of the OK button when pressed */
            QPushButton:pressed {
                background-color: rgb(30, 30, 30);
            }
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Message")
        msg_box.setText(f"{error_message}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(warning_box_style)
        msg_box.exec_()

    def download_url_file(self):
        version_fields = ["id", "sg_uploaded_movie"]
        for sid in self.action.selected_ids_filter:
            version = self.action.sg.find_one(self.action.entity_type, [sid], version_fields)
            mp4_down = self.path + '/' + version["sg_uploaded_movie"]["name"]
            mp4_filter = mp4_down.split('.')
            low_ext = mp4_filter[-1].lower()
            if low_ext != 'mp4':
                pass
            else:
                self.action.sg.download_attachment(version["sg_uploaded_movie"], file_path=mp4_down)


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    try:
        controller = DownLoadController(window, sys.argv)
        controller.action.log.info("ShotgunAction: Firing... %s" % (sys.argv[1]))
    except IndexError as e:
        raise ShotgunActionException("Missing GET arguments")
    controller.action.log.info("ShotgunAction process finished.")
    window.setCentralWidget(controller.view)
    window.setWindowTitle('Mp4 Downloader')
    window.setFixedSize(500, 150)
    window.setStyleSheet("background-color: rgb(50, 50, 50);")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
