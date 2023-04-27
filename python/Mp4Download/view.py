from PySide2.QtWidgets import *


class DownLoadMainView(QWidget):
    def __init__(self):
        super().__init__()
        self.path_line_edit = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.path_hbox_layout = QHBoxLayout()

        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('cancel')
        self.user_controller_btn_hbox_layout = QHBoxLayout()

        self.main_vbox_layout = QVBoxLayout()

    def test_ui(self):
        self.path_line_edit.setPlaceholderText("Select the save folder")

        self.path_hbox_layout.addWidget(self.path_line_edit)
        self.path_hbox_layout.addWidget(self.browse_button)
        self.main_vbox_layout.addLayout(self.path_hbox_layout)

        self.browse_button.clicked.connect(self.test_browse_clicked)

        self.user_controller_btn_hbox_layout.addWidget(self.ok_button)
        self.user_controller_btn_hbox_layout.addWidget(self.cancel_button)
        self.main_vbox_layout.addLayout(self.user_controller_btn_hbox_layout)

        self.ok_button.clicked.connect(self.test_ok_clicked)
        self.cancel_button.clicked.connect(self.test_cancel_clicked)

        self.setLayout(self.main_vbox_layout)

    @staticmethod
    def test_browse_clicked():
        print("find the saved directory")

    @staticmethod
    def test_ok_clicked():
        print("mp4 save")

    @staticmethod
    def test_cancel_clicked():
        print("end to find directory")


class BrowseDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        op = self.Options()
        op |= self.DontUseNativeDialog
        op |= self.ShowDirsOnly
        op = self.getExistingDirectory(None, "Select Directory", "", options=op)
        self.option = op


def main():
    app = QApplication()
    test_ui = DownLoadMainView()
    test_ui.test_ui()
    window = QMainWindow()
    window.setCentralWidget(test_ui)
    window.setWindowTitle('Mp4 Downloader')
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
