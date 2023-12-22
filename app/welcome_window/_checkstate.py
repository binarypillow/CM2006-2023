def check_state(self):
    """Check the state of the UI elements and enable/disable the "continue" and the labels' box button accordingly."""
    if (
        self.ui.seg_text.text().endswith(".nii.gz")
        and self.ui.img_text.text().endswith(".nii.gz")
        and self.get_checked_labels()
    ):
        self.ui.continue_button.setDisabled(False)
        self.ui.labels_box.setDisabled(False)
    else:
        self.ui.continue_button.setDisabled(True)
        self.ui.labels_box.setDisabled(True)
