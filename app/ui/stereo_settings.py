# Form implementation generated from reading ui file '../app/ui\stereo_settings.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from app.utils import get_abs_path


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(337, 136)
        Dialog.setStyleSheet("QMainWindow {\n"
"    background-color: #F8F9FA\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #023047;\n"
"    border-radius: 5px;\n"
"    font: 10px \'Roboto\', sans-serif;\n"
"    color: #023047;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QLabel {\n"
"    font: 11px \'Roboto\', sans-serif;\n"
"    color: black;\n"
"}\n"
"\n"
"QScrollArea {\n"
"    background-color: white;\n"
"    border: trasparent;\n"
"}\n"
"\n"
"QVBoxLayout {\n"
"    background-color: white;\n"
"    border: trasparent;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #219EBC;\n"
"    min-height: 10px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    width: 12px;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical{\n"
"    height: 0px; \n"
"    background: trasparent;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    border: 1px solid #023047;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex;\n"
"    font: 12px \'Roboto\', sans-serif;\n"
"    color: white;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 4px;\n"
"    padding: 2px 6px 2px 6px;\n"
"    color: white;\n"
"    background-color: #023047;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    font: 12px;\n"
"    font-family: \'Roboto\', sans-serif;\n"
"    color: white;\n"
"    background-color: #023047;\n"
"    border-radius: 12px;\n"
"     width: 80px;\n"
"    height: 25px;\n"
"}\n"
"\n"
"QToolButton{\n"
"    font: 12px;\n"
"    font-family: \'Roboto\', sans-serif;\n"
"    font-weight: 400;\n"
"    color: black;\n"
"    background-color: #FB8500;\n"
"    border-radius: 6px;\n"
"     width: 65px;\n"
"    height: 15px;\n"
"}\n"
"\n"
"QPushButton#ok_button{\n"
"    font: 12px;\n"
"    font-family: \'Roboto\', sans-serif;\n"
"    color: black;\n"
"    background-color: #FB8500;\n"
"    border-radius: 12px;\n"
"     width: 100px;\n"
"    height: 25px;\n"
"}\n"
"\n"
"QPushButton:disabled#ok_button{\n"
"    font: 12px;\n"
"    font-family: \'Roboto\', sans-serif;\n"
"     color: rgba(0,0,0,0.5);\n"
"    background-color:rgba( 251, 133, 0, 0.5);\n"
"    border-radius: 12px;\n"
"     width: 100px;\n"
"    height: 25px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked{\n"
"    background-color: #FB8500;\n"
"    border: 1px solid #023047;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled#img_button,  QCheckBox::indicator:disabled#seg_button{\n"
"    background-color: red;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked#img_button,\n"
"QCheckBox::indicator:checked#seg_button {\n"
"    background-color: green;\n"
"    border-radius: 4px;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ipd_label = QtWidgets.QLabel(parent=self.widget)
        self.ipd_label.setStyleSheet("")
        self.ipd_label.setObjectName("ipd_label")
        self.horizontalLayout_2.addWidget(self.ipd_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.ipd_line_edit = QtWidgets.QLineEdit(parent=self.widget)
        self.ipd_line_edit.setMaximumSize(QtCore.QSize(114, 16777215))
        self.ipd_line_edit.setStyleSheet("")
        self.ipd_line_edit.setObjectName("ipd_line_edit")
        self.horizontalLayout_2.addWidget(self.ipd_line_edit, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.line = QtWidgets.QFrame(parent=self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.cancel_button = QtWidgets.QPushButton(parent=self.widget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_4.addWidget(self.cancel_button)
        self.ok_button = QtWidgets.QPushButton(parent=self.widget)
        self.ok_button.setEnabled(True)
        self.ok_button.setStyleSheet("")
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_4.addWidget(self.ok_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Stereo parameters"))
        self.ipd_label.setText(_translate("Dialog", "Interpupillary distance (IPD)"))
        self.label_2.setText(_translate("Dialog", "mm"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.ok_button.setText(_translate("Dialog", "Confirm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
