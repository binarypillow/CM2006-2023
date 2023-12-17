from PyQt6 import QtWidgets
import nibabel as nib
from app.main_window import MainWindow
from app.ui import welcome_interface
from app.utils import get_keys_from_yaml, get_abs_path


class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.img_path = ""
        self.seg_path = ""
        self.next_window = None

        self.setWindowTitle("File selection")  # TODO: fix

        # Load and set up interface
        self.ui = welcome_interface.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.img_file.clicked.connect(lambda: self.select_file("image"))
        self.ui.seg_file.clicked.connect(lambda: self.select_file("segmentation"))
        self.ui.exit_button.clicked.connect(self.close)
        # Connect the "Continue" button to the function to open a new window
        self.ui.continue_button.clicked.connect(self.open_new_window)

        # Create a QWidget and a QVBoxLayout
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()
        # List of labels
        labels = get_keys_from_yaml(get_abs_path("resources/config/labels.yml"))
        # For each label, create a QLabel and add it to the layout
        for label in labels:
            checkbox_widget = QtWidgets.QCheckBox(label)
            checkbox_widget.setChecked(True)
            scroll_layout.addWidget(checkbox_widget)
        # Set the layout to the widget
        scroll_widget.setLayout(scroll_layout)
        # Set the widget to the QScrollArea
        self.ui.labels_list.setWidget(scroll_widget)

    def select_file(self, file_type):
        """
        Selects a file of the specified type and updates the UI accordingly.

        Args:
            file_type (str): The type of file to select.

        Returns:
            None
        """

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if file_type == "image":
                self.img_path = file_path
                self.ui.img_text.insert(self.img_path)
                button = self.ui.img_button
                alert = self.ui.img_alert
            else:
                self.seg_path = file_path
                self.ui.seg_text.insert(self.seg_path)
                button = self.ui.seg_button
                alert = self.ui.seg_alert

            if file_path.endswith(".nii.gz"):
                button.setChecked(True)
                alert.setStyleSheet("color: green;")
                alert.setText("Valid file format!")
            else:
                alert.setStyleSheet("color: red;")
                alert.setText("Invalid file format!")
            self.check_files()

    def check_files(self):
        """
        Checks if the selected files have valid file formats.

        This method checks if both the segmentation file and the image file have valid file formats.
        If both files have valid formats, it enables the "continue button" and the "labels box".
        Otherwise, it disables the "continue" button.

        Returns:
            None
        """
        if self.seg_path.endswith(".nii.gz") and self.img_path.endswith(".nii.gz"):
            self.ui.continue_button.setDisabled(False)
            self.ui.labels_box.setDisabled(False)
        else:
            self.ui.continue_button.setDisabled(True)

    def open_new_window(self):
        """
        Opens a new window.

        This method creates a new instance of the MainWindow class with the selected image file, segmentation file,
        and checked labels. It shows the new window, closes the current window, and transitions to the main window.

        Returns:
            None
        """
        # The next window is the main window
        self.next_window = MainWindow(
            self.img_path,
            self.seg_path,
            self.get_checked_labels(),
        )
        self.next_window.show()
        self.close()

    def get_checked_labels(self):
        """
        Retrieves the checked labels from the labels list.

        This method iterates through the labels list and collects the text of the checked checkboxes.
        It returns a list of the checked labels.

        Returns:
            list: A list of the checked labels.
        """
        checked_labels = []
        scroll_layout = self.ui.labels_list.widget().layout()
        for i in range(scroll_layout.count()):
            widget = scroll_layout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QCheckBox) and widget.isChecked():
                checked_labels.append(widget.text())
        return checked_labels
