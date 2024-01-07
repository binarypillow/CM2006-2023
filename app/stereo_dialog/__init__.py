from PyQt6 import QtWidgets, QtCore
from app.ui import stereo_settings


class StereoParam(QtWidgets.QDialog):
    """Dialog window for setting stereo parameters."""

    # Signal sent to the first window with the values of IPD and angle
    value = QtCore.pyqtSignal(float)

    def __init__(self, ipd_value):
        super(StereoParam, self).__init__()

        # ---- Interface initialization ----
        self.setWindowTitle("Stereo parameters")
        self.ui = stereo_settings.Ui_Dialog()
        self.ui.setupUi(self)
        # Write current value
        self.ui.ipd_line_edit.setText(str(ipd_value))
        # Check if the value is valid when it's changed
        self.ui.ipd_line_edit.textChanged.connect(self.updateOKButtonVisibility)
        # Connect the "Continue" button to the function to set the values and close the window
        self.ui.ok_button.clicked.connect(self.sendValues)
        # Connect the "Cancel" button to the function to close the window
        self.ui.cancel_button.clicked.connect(self.close)

    # ---- Methods ----
    def updateOKButtonVisibility(self):
        """
        Updates the visibility of the OK button based on the validity of the input in the LineEdit.

        Args:
            self: The instance of the class.

        Returns:
            None
        """

        # Check if the input field contains a number
        ipd_text = self.ui.ipd_line_edit.text()

        try:
            _ = float(ipd_text)
            # Enable the button
            self.ui.ok_button.setDisabled(False)
        except ValueError:
            # Throw an error and disable the button
            self.ui.ok_button.setDisabled(True)

    def sendValues(self):
        """
        Sends the value from the input field as a signal and closes the dialogue.

        Args:
            self: The instance of the class.

        Returns:
            None
        """

        ipd_text = self.ui.ipd_line_edit.text()
        self.value.emit(float(ipd_text))
        self.close()
