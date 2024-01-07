from PyQt6 import QtWidgets
from app.ui import about_text


class AboutText(QtWidgets.QDialog):
    """A dialogue window displaying information about the application."""

    def __init__(self):
        super(AboutText, self).__init__()

        # ---- Interface initialization ----
        self.setWindowTitle("About")
        self.ui = about_text.Ui_Dialog()
        self.ui.setupUi(self)

        # Connect the "OK" button to the function to close the current window
        self.ui.ok_button.clicked.connect(self.close)
