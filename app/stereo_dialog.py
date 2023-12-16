from PyQt6 import QtWidgets, QtCore
from app.ui import stereo_settings


class StereoParam(QtWidgets.QDialog):
    # Signal sent to the first window with the values of IPD and angle
    values = QtCore.pyqtSignal(float, float)

    def __init__(self):
        super(StereoParam, self).__init__()
        self.setWindowTitle("Stereo parameters")
        self.ui = stereo_settings.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.ipd_line_edit.textChanged.connect(self.updateOKButtonVisibility)
        self.ui.angle_line_edit.textChanged.connect(self.updateOKButtonVisibility)
        self.ui.ok_button.setVisible(False)
        self.ui.ok_button.clicked.connect(self.sendValues)

    def updateOKButtonVisibility(self):
        # Check if the two LineEdits contain numbers
        ipd_text = self.ui.ipd_line_edit.text()
        angle_text = self.ui.angle_line_edit.text()

        try:
            ipd_value = float(ipd_text)
            angle_value = float(angle_text)
            self.ui.ok_button.setVisible(True)
        except ValueError:
            self.ui.ok_button.setVisible(False)

    def sendValues(self):
        ipd_text = self.ui.ipd_line_edit.text()
        angle_text = self.ui.angle_line_edit.text()
        self.values.emit(float(ipd_text), float(angle_text))
