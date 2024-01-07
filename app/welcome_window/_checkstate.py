def check_state(self):
    """
    Checks the state of the UI elements and enables or disables the "Continue" button and organs' selection box
    accordingly.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    if (
        self.ui.seg_text.text().endswith(".nii.gz")
        and self.ui.img_text.text().endswith(".nii.gz")
        and self.get_checked_labels()
    ):
        # Enable the "Continue" button and the organs' selection box
        self.ui.continue_button.setDisabled(False)
        self.ui.labels_box.setDisabled(False)
    elif self.ui.seg_text.text().endswith(
        ".nii.gz"
    ) and self.ui.img_text.text().endswith(".nii.gz"):
        # Disable the "Continue" button
        self.ui.continue_button.setDisabled(True)
    else:
        # Disable the "Continue" button and the organs' selection box
        self.ui.continue_button.setDisabled(True)
        self.ui.labels_box.setDisabled(True)
