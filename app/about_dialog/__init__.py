from PyQt6 import QtWidgets
from app.ui import about_text


class AboutText(QtWidgets.QDialog):
    """A dialog window displaying information about the application."""

    def __init__(self):
        super(AboutText, self).__init__()

        # ---- Variables initialization ----

        # ---- Interface initialization ----
        self.setWindowTitle("About")
        self.ui = about_text.Ui_Dialog()
        self.ui.setupUi(self)
        # Connect the "Ok" button to the function to close the current window
        self.ui.ok_button.clicked.connect(self.close)

    # ---- Methods imports ----
