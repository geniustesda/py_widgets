# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Qrcode_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Qrcode(object):
    def setupUi(self, Qrcode):
        Qrcode.setObjectName("Qrcode")
        Qrcode.resize(300, 335)
        self.QrcodeShow = QtWidgets.QLabel(Qrcode)
        self.QrcodeShow.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.QrcodeShow.setMinimumSize(QtCore.QSize(200, 200))
        self.QrcodeShow.setText("")
        self.QrcodeShow.setObjectName("QrcodeShow")
        self.QrcodeAddressText = QtWidgets.QLineEdit(Qrcode)
        self.QrcodeAddressText.setGeometry(QtCore.QRect(0, 300, 301, 31))
        self.QrcodeAddressText.setObjectName("QrcodeAddressText")

        self.retranslateUi(Qrcode)
        QtCore.QMetaObject.connectSlotsByName(Qrcode)

    def retranslateUi(self, Qrcode):
        _translate = QtCore.QCoreApplication.translate
        Qrcode.setWindowTitle(_translate("Qrcode", "Qrcode"))