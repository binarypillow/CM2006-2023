from PyQt6 import QtWidgets, QtCore
from app.ui import about_text


class AboutText(QtWidgets.QDialog):
    def __init__(self):
        super(AboutText, self).__init__()
        self.setWindowTitle("About")
        self.ui = about_text.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.ok_button.clicked.connect(self.close)
