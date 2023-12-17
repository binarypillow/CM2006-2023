from PyQt6 import QtWidgets, QtCore
from app.ui import stereo_settings


class StereoParam(QtWidgets.QDialog):
    # Signal sent to the first window with the values of IPD and angle
    value = QtCore.pyqtSignal(float)

    def __init__(self, ipd_value):
        super(StereoParam, self).__init__()
        self.setWindowTitle("Stereo parameters")
        self.ui = stereo_settings.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.ipd_line_edit.setText(str(ipd_value))

        self.ui.ipd_line_edit.textChanged.connect(self.updateOKButtonVisibility)
        self.ui.ok_button.clicked.connect(self.sendValues)
        self.ui.cancel_button.clicked.connect(self.close)

    def updateOKButtonVisibility(self):
        # Check if the two LineEdits contain numbers
        ipd_text = self.ui.ipd_line_edit.text()

        try:
            ipd_value = float(ipd_text)
            self.ui.ok_button.setDisabled(False)
        except ValueError:
            self.ui.ok_button.setDisabled(True)

    def sendValues(self):
        ipd_text = self.ui.ipd_line_edit.text()
        self.value.emit(float(ipd_text))
        self.close()
