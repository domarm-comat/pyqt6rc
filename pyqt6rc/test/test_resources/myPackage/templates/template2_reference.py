# Form implementation generated from reading ui file 'template2.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from importlib.resources import path

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(292, 208)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        with path("crawlMpGui.resources", "image1.png") as f_path:
            self.label.setPixmap(QtGui.QPixmap(str(f_path)))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        with path("crawlMpGui.resources", "image1_r2.png") as f_path:
            icon.addPixmap(
                QtGui.QPixmap(str(f_path)),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText("")
        #         self.label_2.setPixmap(QtGui.QPixmap(":/images_non_existent/image2.png"))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        icon1 = QtGui.QIcon()
        with path("crawlMpGui.resources.icons", "icon2_r2.png") as f_path:
            icon1.addPixmap(
                QtGui.QPixmap(str(f_path)),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
        with path("crawlMpGui.resources.icons", "icon1.png") as f_path:
            icon1.addPixmap(
                QtGui.QPixmap(str(f_path)),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.On,
            )
        self.pushButton_4.setIcon(icon1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        icon2 = QtGui.QIcon()
        with path("crawlMpGui.resources.icons", "icon1.png") as f_path:
            icon2.addPixmap(
                QtGui.QPixmap(str(f_path)),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
        self.pushButton.setIcon(icon2)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        icon3 = QtGui.QIcon()
        with path("crawlMpGui.resources.icons", "icon2.png") as f_path:
            icon3.addPixmap(
                QtGui.QPixmap(str(f_path)),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setText("")
        with path("crawlMpGui.resources", "image1_r2.png") as f_path:
            self.label_3.setPixmap(QtGui.QPixmap(str(f_path)))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setText("")
        with path("crawlMpGui.resources", "image2_r2.png") as f_path:
            self.label_4.setPixmap(QtGui.QPixmap(str(f_path)))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "PushButton"))
        self.pushButton_4.setText(_translate("Form", "PushButton"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.pushButton_2.setText(_translate("Form", "PushButton"))
