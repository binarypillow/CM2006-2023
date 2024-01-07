import sys
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from app.welcome_window import WelcomeWindow
from app.utils import get_abs_path


def main():
    """
    Runs the main application.

    This function initialises the application, sets the window icon, creates and shows the welcome window
    and then exits the application after the event loop is finished.
    """

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_abs_path("resources/icons/window/logo.svg")))

    welcome = WelcomeWindow()
    # Set the window title
    welcome.setWindowTitle("File selection")
    welcome.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main())
