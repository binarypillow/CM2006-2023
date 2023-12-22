from PyQt6 import QtWidgets


def select_file(self, file_type):
    """Select a file and update the UI based on the file type."""
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
            button.setChecked(False)
            alert.setStyleSheet("color: red;")
            alert.setText("Invalid file format!")
        self.check_state()
