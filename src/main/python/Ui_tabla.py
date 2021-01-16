# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabla.ui',
# licensing of 'tabla.ui' applies.
#
# Created: Sat Jul 25 19:14:52 2020
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TableDialog(object):
    def setupUi(self, TableDialog):
        TableDialog.setObjectName("TableDialog")
        TableDialog.resize(1259, 733)
        self.tabla = QtWidgets.QTableWidget(TableDialog)
        self.tabla.setGeometry(QtCore.QRect(10, 10, 1211, 651))
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.cerrar = QtWidgets.QPushButton(TableDialog)
        self.cerrar.setGeometry(QtCore.QRect(800, 690, 113, 32))
        self.cerrar.setObjectName("cerrar")
        self.exportar = QtWidgets.QPushButton(TableDialog)
        self.exportar.setGeometry(QtCore.QRect(930, 690, 131, 32))
        self.exportar.setObjectName("exportar")
        self.progressBar = QtWidgets.QProgressBar(TableDialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 680, 741, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(TableDialog)
        QtCore.QMetaObject.connectSlotsByName(TableDialog)

    def retranslateUi(self, TableDialog):
        TableDialog.setWindowTitle(QtWidgets.QApplication.translate("TableDialog", "Tabla Validacion", None, -1))
        self.cerrar.setText(QtWidgets.QApplication.translate("TableDialog", "Cerrar", None, -1))
        self.exportar.setText(QtWidgets.QApplication.translate("TableDialog", "Exportar a excel", None, -1))

