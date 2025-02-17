# Form implementation generated from reading ui file '../app/ui\about_text.ui'
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
        Dialog.resize(304, 244)
        Dialog.setStyleSheet("QMainWindow {\n"
"    background-color: #F8F9FA;\n"
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
"     color: black;\n"
"    background-color: #FB8500;\n"
"    border-radius: 10px;\n"
"     width: 60px;\n"
"    height: 25px;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_text = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.name_text.setFont(font)
        self.name_text.setStyleSheet("font: 22px")
        self.name_text.setObjectName("name_text")
        self.verticalLayout.addWidget(self.name_text, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.version_text = QtWidgets.QLabel(parent=Dialog)
        self.version_text.setObjectName("version_text")
        self.verticalLayout.addWidget(self.version_text, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.info_text = QtWidgets.QLabel(parent=self.groupBox)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.info_text.setFont(font)
        self.info_text.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.info_text.setScaledContents(False)
        self.info_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.info_text.setWordWrap(True)
        self.info_text.setObjectName("info_text")
        self.verticalLayout_3.addWidget(self.info_text)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.ok_button = QtWidgets.QPushButton(parent=Dialog)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_2.addWidget(self.ok_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.name_text.setText(_translate("Dialog", "<App_name>"))
        self.version_text.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-style:italic;\">Version 0.0.1</span></p></body></html>"))
        self.info_text.setText(_translate("Dialog", "This application is a work in progress and is not ready for production yet. Use it at your own risk."))
        self.ok_button.setText(_translate("Dialog", "Ok"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
