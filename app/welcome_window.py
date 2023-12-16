from PyQt6 import QtWidgets
from app.main_window import MainWindow
from app.ui import welcome_interface


class WelcomeWindow(QtWidgets.QDialog):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.setWindowTitle("File choice")
        self.ui = welcome_interface.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.continue_button.setVisible(False)
        self.ui.img_button.clicked.connect(self.select_image_file)
        self.ui.seg_button.clicked.connect(self.select_segmentation_file)

        self.img_path = ""
        self.label_path = ""
        self.next_window = None

        # Connect the "Continue" button to the function to open a new window
        self.ui.continue_button.clicked.connect(self.open_new_window)

    def select_image_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)

        # If file is open
        if file_dialog.exec():
            # Get the path of the selected file
            self.img_path = file_dialog.selectedFiles()[0]
            if self.img_path.endswith(".nii.gz"):
                self.ui.img_box.setChecked(True)
            # Update continue button if both files were selected
            self.check_files()

    def select_segmentation_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)

        # If file is open
        if file_dialog.exec():
            # Get the path of the selected file
            self.label_path = file_dialog.selectedFiles()[0]

            if self.label_path.endswith(".nii.gz"):
                self.ui.seg_box.setChecked(True)
            # Update continue button if both files were selected
            self.check_files()

    def check_files(self):
        if self.label_path.endswith(".nii.gz") and self.img_path.endswith(".nii.gz"):
            self.ui.continue_button.setVisible(True)
        else:
            self.ui.continue_button.setVisible(False)

    def open_new_window(self):
        # The next window is the main window
        self.next_window = MainWindow(self.img_path, self.label_path)
        self.next_window.show()
        self.close()
