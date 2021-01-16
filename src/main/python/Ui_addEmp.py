# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regEmp.ui',
# licensing of 'regEmp.ui' applies.
#
# Created: Tue Jul 21 08:43:46 2020
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(756, 435)
        self.tabla = QtWidgets.QTableWidget(Dialog)
        self.tabla.setGeometry(QtCore.QRect(220, 40, 531, 331))
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.btnGuardar = QtWidgets.QPushButton(Dialog)
        self.btnGuardar.setGeometry(QtCore.QRect(20, 390, 91, 32))
        self.btnGuardar.setObjectName("btnGuardar")
        self.entNombre = QtWidgets.QLineEdit(Dialog)
        self.entNombre.setGeometry(QtCore.QRect(20, 50, 191, 31))
        self.entNombre.setText("")
        self.entNombre.setObjectName("entNombre")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 59, 16))
        self.label.setObjectName("label")
        self.entRuc = QtWidgets.QLineEdit(Dialog)
        self.entRuc.setGeometry(QtCore.QRect(20, 120, 191, 31))
        self.entRuc.setText("")
        self.entRuc.setObjectName("entRuc")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 59, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 59, 16))
        self.label_3.setObjectName("label_3")
        self.entClave = QtWidgets.QLineEdit(Dialog)
        self.entClave.setGeometry(QtCore.QRect(20, 190, 191, 31))
        self.entClave.setText("")
        self.entClave.setObjectName("entClave")
        self.entToken = QtWidgets.QLineEdit(Dialog)
        self.entToken.setGeometry(QtCore.QRect(20, 260, 191, 31))
        self.entToken.setText("")
        self.entToken.setObjectName("entToken")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 240, 81, 16))
        self.label_4.setObjectName("label_4")
        self.btnSelectDir = QtWidgets.QPushButton(Dialog)
        self.btnSelectDir.setGeometry(QtCore.QRect(10, 320, 201, 32))
        self.btnSelectDir.setObjectName("btnSelectDir")
        self.btnActualizar = QtWidgets.QPushButton(Dialog)
        self.btnActualizar.setGeometry(QtCore.QRect(120, 390, 91, 32))
        self.btnActualizar.setObjectName("btnActualizar")
        self.lblNombre = QtWidgets.QLabel(Dialog)
        self.lblNombre.setGeometry(QtCore.QRect(10, 360, 201, 20))
        self.lblNombre.setObjectName("lblNombre")
        self.btnEliminar = QtWidgets.QPushButton(Dialog)
        self.btnEliminar.setGeometry(QtCore.QRect(430, 390, 91, 32))
        self.btnEliminar.setObjectName("btnEliminar")
        self.btnEditar = QtWidgets.QPushButton(Dialog)
        self.btnEditar.setGeometry(QtCore.QRect(330, 390, 91, 32))
        self.btnEditar.setObjectName("btnEditar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.btnGuardar.setText(QtWidgets.QApplication.translate("Dialog", "Guardar", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Nombre", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "RUC", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "client_id", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "client_secret", None, -1))
        self.btnSelectDir.setText(QtWidgets.QApplication.translate("Dialog", "Seleccionar Carpeta", None, -1))
        self.btnActualizar.setText(QtWidgets.QApplication.translate("Dialog", "Actualizar", None, -1))
        self.lblNombre.setText(QtWidgets.QApplication.translate("Dialog", "No se ha seleccionado ... carpeta", None, -1))
        self.btnEliminar.setText(QtWidgets.QApplication.translate("Dialog", "Eliminar", None, -1))
        self.btnEditar.setText(QtWidgets.QApplication.translate("Dialog", "Editar", None, -1))

