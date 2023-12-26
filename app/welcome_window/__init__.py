from PyQt6 import QtCore, QtWidgets
from app.ui import welcome_interface
from app.utils import get_keys_from_yaml, get_abs_path
from app.main_window import MainWindow


class WelcomeWindow(QtWidgets.QMainWindow):
    """A class representing the welcome window of the application."""

    def __init__(self):
        super(WelcomeWindow, self).__init__()

        # ---- Variables initialization ----
        self.img_path = ""
        self.seg_path = ""
        self.next_window = None
        self.history_path = "history.yaml"

        # ---- Interface initialization ----
        self.ui = welcome_interface.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.img_file.clicked.connect(lambda: self.select_file("image"))
        self.ui.seg_file.clicked.connect(lambda: self.select_file("segmentation"))
        # Connect the "Continue" button to the function to open a new window
        self.ui.continue_button.clicked.connect(self.open_new_window)
        # Connect the "Exit" button to the function to close the current window
        self.ui.exit_button.clicked.connect(self.close)

        # Load the saved history if present
        history = self.load_history()
        # Dynamically create the labels' list
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()
        # Get the list of labels
        labels_list = get_keys_from_yaml(get_abs_path("/resources/config/labels.yml"))
        # For each label, create a QLabel and add it to the layout
        for label in labels_list:
            checkbox_widget = QtWidgets.QCheckBox(label)
            if history and label in history["checked_labels"] or not history:
                checkbox_widget.setChecked(True)
            else:
                checkbox_widget.setChecked(False)
            checkbox_widget.stateChanged.connect(self.check_state)
            # Add the widget to the scroll down
            scroll_layout.addWidget(checkbox_widget)
        # Set the layout to the widget
        scroll_widget.setLayout(scroll_layout)
        # Set the widget to the QScrollArea
        self.ui.labels_list.setWidget(scroll_widget)

        # ---- State initialization ----
        self.check_state()

    # ---- Methods imports ----
    from ._selectfiles import select_file
    from ._checkstate import check_state
    from ._getcheckedlabels import get_checked_labels
    from ._history import save_history, load_history

    def open_new_window(self):
        """Open a new window and save the current state into a YAML file."""
        # Save the paths and the checked files into a YAML file
        self.save_history()

        self.next_window = MainWindow(
            self.img_path,
            self.seg_path,
            self.get_checked_labels(),
        )
        # Set the window title
        self.next_window.setWindowTitle("Visualization application")
        self.next_window.show()
        self.close()
