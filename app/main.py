import sys
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from app.welcome_window import WelcomeWindow
from app.main_window import MainWindow
from app.utils import get_abs_path


def main():
    """
    Runs the main application.

    This function initializes the application, sets the window icon, creates and shows the welcome window,
    and then exits the application after the event loop is finished.
    """

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_abs_path("resources/icons/window/logo.svg")))

    welcome = WelcomeWindow()

    welcome.show()

    # Use this to display only the second window
    # img_path = "data/images/FLARE22_Tr_0001_0000.nii.gz"
    # label_path = "data/labels/FLARE22_Tr_0001.nii.gz"

    # main_window = MainWindow(img_path, label_path)
    # main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main())
