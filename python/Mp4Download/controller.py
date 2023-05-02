# !/usr/bin/env python
# :coding: utf-8

from model import DownLoadModel
from view import *
from PySide2.QtWidgets import *
import sys
import os
import urllib.parse
import logging as logger
from shotgun_api3 import shotgun


class DownLoadController:
    def __init__(self, main_window, url):
        # url is variable
        shotgrid_url = "https://rndtest.shotgrid.autodesk.com/"
        scripts_name = "script_psj"
        scripts_key = "qJq9qnmuv*aaxqkulybgdymlr"

        self.sg = shotgun.Shotgun(shotgrid_url, script_name=scripts_name, api_key=scripts_key)

        self.log_file = ''
        self.log_file_setting()
        self.logger = self._init_log(self.log_file)
        self.url = url
        self.protocol, self.action, self.params = self._parse_url()

        self.entity_type = ''
        self.selected_ids = ''
        self.selected_ids_filter = []

        model = DownLoadModel()
        self.main_window = main_window
        self.view = DownLoadMainView()

        self.dialog = None

        self.path = model.path

        self.browse_sig = False

        self.main_ui()

        self.init_set()

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

    @staticmethod
    def _init_log(filename):
        try:
            logger.basicConfig(
                level=logger.DEBUG,
                format="%(asctime)s %(levelname)-8s %(message)s",
                datefmt="%Y-%b-%d %H:%M:%S",
                filename=filename,
                filemode="w+",
            )
        except IOError as e:
            raise ShotgunActionException("Unable to open logfile for writing: %s" % e)
        logger.info("ShotgunAction logging started.")
        return logger

    def _parse_url(self):
        logger.info("Parsing full url received: %s" % self.url)

        # get the protocol used
        protocol, path = self.url.split(":", 1)
        logger.info("protocol: %s" % protocol)

        # extract the action
        action, params = path.split("?", 1)
        action = action.strip("/")
        logger.info("action: %s" % action)

        # extract the parameters
        # 'column_display_names' and 'cols' occurs once for each column displayed so we store it as a list
        params = params.split("&")
        p = {"column_display_names": [], "cols": []}
        for arg in params:
            key, value = map(urllib.parse.unquote, arg.split("=", 1))
            if key == "column_display_names" or key == "cols":
                p[key].append(value)
            else:
                p[key] = value
        params = p
        logger.info("params: %s" % params)
        return protocol, action, params

    def init_set(self):
        # entity type that the page was displaying
        self.entity_type = self.params["entity_type"]

        # ids of entities that were currently selected
        if len(self.params["selected_ids"]) > 0:
            sids = self.params["selected_ids"].split(",")
            self.selected_ids = [int(sid) for sid in sids]

        # All selected ids of the entities returned by the query in filter format ready
        # to use in a find() query
        self.selected_ids_filter = self._convert_ids_to_filter(self.selected_ids)

    def log_file_setting(self):
        log_dir = os.path.dirname(sys.argv[0]) + os.sep + 'action_log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        else:
            self.log_file = log_dir + os.sep + 'shotgun_action.log'

    # ----------------------------------------------
    # Convert IDs to filter format to us in find() queries
    # ----------------------------------------------
    @staticmethod
    def _convert_ids_to_filter(idents):
        filter_list = []
        for ident in idents:
            filter_list.append(["id", "is", ident])
        logger.debug("parsed ids into: %s" % filter_list)
        return filter_list

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
        for sid in self.selected_ids_filter:
            version = self.sg.find_one(self.entity_type, [sid], version_fields)
            self.path = self.path + '/' + version["sg_uploaded_movie"]["name"]
            self.sg.download_attachment(version["sg_uploaded_movie"], file_path=self.path)


class ShotgunActionException(Exception):
    pass


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    try:
        controller = DownLoadController(window, sys.argv[1])
        logger.info("ShotgunAction: Firing... %s" % (sys.argv[1]))
    except IndexError as e:
        raise ShotgunActionException("Missing GET arguments")
    logger.info("ShotgunAction process finished.")

    window.setCentralWidget(controller.view)
    window.setWindowTitle('Mp4 Downloader')
    window.setFixedSize(500, 150)
    window.setStyleSheet("background-color: rgb(50, 50, 50);")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
