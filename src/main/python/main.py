from fbs_runtime.application_context.PySide2 import ApplicationContext
import sys
from PySide2.QtWidgets import QApplication, QDialog,QFileDialog,QMainWindow,QTableWidgetItem,QErrorMessage,QMessageBox
from Ui_window import Ui_MainWindow
from Ui_addEmp import Ui_Dialog
from Ui_tabla import Ui_TableDialog
from metodos import Metodos
import os
import json
import pandas as pd
import numpy as np
from PySide2.QtCore import Qt, QThread,QProcess,QObject,QTimer
from PySide2.QtWidgets import QProgressDialog
from threading import Thread
import time

class AddEmp(QDialog):
    def __init__(self, parent=None):
      super(AddEmp, self).__init__(parent)
      self.ui = Ui_Dialog()
      self.ui.setupUi(self)
      self.Mtos = Metodos()
      self.updateTable()
      self.ui.btnSelectDir.clicked.connect(self.selectCarpeta)
      self.ui.btnEliminar.clicked.connect(lambda:self.edit(True))
      self.ui.btnEditar.clicked.connect(self.edit)
      self.ui.btnGuardar.clicked.connect(self.save)
      self.ui.btnActualizar.clicked.connect(lambda:self.save(True))
      self.currentId = None
      self.ui.btnActualizar.setEnabled(False)
    def updateTable(self):
      resultado = self.Mtos.run_query('select * from empresas')
      if resultado:
        self.Mtos.printOnTable(self.ui.tabla,self.Mtos.generarHeaders('empresas'),resultado)
    def save(self,update=False):
      nombre=self.ui.entNombre.text()
      ruc = self.ui.entRuc.text()
      sol = self.ui.entClave.text()
      token = self.ui.entToken.text()
      path = self.ui.lblNombre.text()
      values = (nombre,ruc,sol,token,path,)
      if all(values):
        try:
          text_files = [f for f in os.listdir(path) if f.endswith('.dbf')]
          if 'tbregdatos.dbf' in text_files:
            if update:
              self.Mtos.updRegistro("empresas",self.currentId,tuple(values))
              self.ui.btnGuardar.setEnabled(True)
              self.ui.btnActualizar.setEnabled(False)
            else:
              self.Mtos.addRegistro("empresas",tuple(values))
            self.updateTable()
            self.ui.entNombre.setText("")
            self.ui.entRuc.setText("")
            self.ui.entClave.setText("")
            self.ui.entToken.setText("")
            self.ui.lblNombre.setText("")
          else:
            nuevo = QErrorMessage(self)
            nuevo.setModal(True)
            nuevo.showMessage("La carpeta no contiene el archivo 'tbregdatos.dbf'")
            self.ui.lblNombre.setText("Seleccione carpeta con tbregdatos.dbf")
        except Exception as e:
          error = QErrorMessage(self)
          error.showMessage(f'Seleccione carpeta con tbregdatos.dbf')
      else:
        nuevo = QErrorMessage(self)
        nuevo.setModal(True)
        nuevo.showMessage("Complete todos los Campos")
    def edit(self,delete=False):
      row, id = self.currentItem()
      if id:
        if delete:
          res = QMessageBox.question(self,"Correcto",f"Desea eliminar {self.ui.tabla.item(row,1).text()}?")
        else:
          res = QMessageBox.question(self,"Correcto",f"Desea modificar {self.ui.tabla.item(row,1).text()}?")

        if res == 16384:
            if delete:
              self.Mtos.delRegistro("empresas",(id,))
              self.ui.tabla.removeRow(row)
            else:
              self.ui.entNombre.setText(self.ui.tabla.item(row,1).text())
              self.ui.entRuc.setText(self.ui.tabla.item(row,2).text())
              self.ui.entClave.setText(self.ui.tabla.item(row,3).text())
              self.ui.entToken.setText(self.ui.tabla.item(row,4).text())
              self.ui.lblNombre.setText(self.ui.tabla.item(row,5).text())
              self.currentId = id
              self.ui.btnGuardar.setEnabled(False)
              self.ui.btnActualizar.setEnabled(True)
              self.ui.tabla.removeRow(row)
      else:
        QMessageBox.information(self,"No seleccion","No se ha seleccionado ningún item")

    def currentItem(self):
      if self.ui.tabla.selectedItems():
        row = self.ui.tabla.currentRow()
        id = self.ui.tabla.item(row,0).text()
        return row,id
      return -1,False
    def selectCarpeta(self):
      path = QFileDialog.getExistingDirectory(self)
      if (path==""):
        nuevo = QErrorMessage(self)
        nuevo.setModal(True)
        nuevo.showMessage("La carpeta no contiene el archivo 'tbregdatos.dbf'")
        self.ui.lblNombre.setText("Seleccione carpeta con el archivo 'tbregdatos.dbf'")
      else:
        self.ui.lblNombre.setText(path)
        text_files = [f for f in os.listdir(path) if f.endswith('.dbf')]
        if 'tbregdatos.dbf' in text_files:
          pass
        else:
          nuevo = QErrorMessage(self)
          nuevo.setModal(True)
          nuevo.showMessage("La carpeta no contiene el archivo 'tbregdatos.dbf'")
          self.ui.lblNombre.setText("Seleccione carpeta con el archivo 'tbregdatos.dbf'")
class Tabla(QDialog):
    def __init__(self, parent=None,listInfo=None):
      super(Tabla, self).__init__(parent)
      self.ui = Ui_TableDialog()
      self.ui.setupUi(self)
      self.Mtos = Metodos()
      self.token = listInfo[0]
      self.ruc = listInfo[1]
      self.path = listInfo[2]
      self.periodo = listInfo[3]
      self.setModal(True)
      self.ui.exportar.setEnabled(False)
      self.ui.cerrar.clicked.connect(self.cerrar)
      self.ui.exportar.clicked.connect(self.export)
      QTimer.singleShot(50,self.readWrite)
    def readWrite(self):
      try:
        table = self.Mtos.readDBF(self.path+'/tbregdatos.dbf')
        self.dataframe = self.Mtos.getColumns(table,['RUC_EMPR','COD_OPER','SER_DOCU','NUM_DOCU','FCH_EMIS','IMP_MONA','IMP_MOEX','REG_CONT','MES_ANO'])
        self.dataframe = self.Mtos.selectBy(self.dataframe,'REG_CONT','RC')
        self.dataframe = self.Mtos.selectBy(self.dataframe,'MES_ANO',self.periodo)
        if (len(self.dataframe)>1):
          self.dataframe["SUNAT"] = np.nan
          self.x = ThreadRead(tablawidget=self.ui.tabla,data=self.dataframe,boton=self.ui.exportar,token=self.token,ruc=self.ruc)
          self.x.start()
        else:
          self.error(f"No se encuentran datos en el periodo {self.periodo}")
      except Exception as e:
        self.error(e)
    def updateProgress(self,i):
      self.ui.progressBar.setValue(i)
      print("progress",i)
    def cerrar(self):
      self.close()
    def export(self):
      filename = QFileDialog.getSaveFileName(self,'Guardar Archivo',f'Validacion-{self.periodo}','.xls(*.xls)')
      try:
        if(filename[0]!=''):
          self.Mtos.savetoXLS(filename[0],self.ui.tabla,self.dataframe)
          self.mensaje("Archivo guardado con exito")
      except Exception as e:
        self.error(f"Ocurrio un error exportando: \n {e}")
    def error(self,msg):
      nuevo = QErrorMessage(self)
      nuevo.setModal(True)
      nuevo.showMessage(msg)
    def mensaje(self,msg):
      nuevo = QMessageBox(self)
      nuevo.setIcon(QMessageBox.Information)
      nuevo.setModal(True)
      nuevo.setText(msg)
      nuevo.show()
class ThreadRead(QThread):
  def __init__(self,parent=None,tablawidget=None,data=None,boton=None,token = None,ruc=None):
    super(ThreadRead,self).__init__(parent)
    self.Mtos = Metodos()
    self.tablawidget = tablawidget
    self.dataframe = data
    self.btnexp = boton
    self.token = token
    self.ruc = ruc
  def run(self):
    self.Mtos.reqAndPrint(self.tablawidget,list(self.dataframe),self.dataframe.values.tolist(),self.token,self.ruc)
    self.btnexp.setEnabled(True)
class Principal (QMainWindow):
  def __init__(self):
    super(Principal, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.Mtos = Metodos()
    self.lista = []
    self.allIds = [False]
    self.ui.btnValidar.setEnabled(False)
    self.ui.btnAdd.clicked.connect(self.addEmp)
    self.ui.btnSelect.clicked.connect(self.selectCarpeta)
    self.ui.cbEmpresa.currentTextChanged.connect(self.cbSelected)
    self.updateCombo()
    self.ui.btnValidar.clicked.connect(self.validar)
  def addEmp(self):
    dialog = AddEmp(self)
    dialog.setModal(True)
    dialog.show()
    dialog.exec_()
    self.updateCombo()
    dialog.close()
  def selectCarpeta(self):
      path = QFileDialog.getExistingDirectory(self)
      if (path==""):
        self.error("La carpeta no contiene el archivo 'tbregdatos.dbf'")
      else:
        self.ui.lblnombre.setText(path)
        text_files = [f for f in os.listdir(path) if f.endswith('.dbf')]
        if 'tbregdatos.dbf' in text_files:
          self.ui.btnValidar.setEnabled(True)
        else:
          self.error("La carpeta no contiene el archivo 'tbregdatos.dbf'")
          self.ui.lblnombre.setText("Seleccione carpeta con el archivo 'tbregdatos.dbf'")
          self.ui.btnValidar.setEnabled(False)
  def updateCombo(self):
    resultado = self.Mtos.run_query('select * from empresas')
    self.ui.cbEmpresa.clear()
    self.ui.cbEmpresa.addItem("Seleccionar empresa ...")
    self.allIds = [False]
    for i in resultado:
      self.allIds.append(i[0])
      self.ui.cbEmpresa.addItem(i[1])
  def cbSelected(self):
    ind=self.ui.cbEmpresa.currentIndex()
    id=self.allIds[ind]
    if id:
      resultado = list(self.Mtos.run_query(f'select * from empresas where id=?',(id,))[0])
      self.ui.entRuc.setText(resultado[2])
      self.ui.entSol.setText(resultado[3])
      self.ui.entToken.setText(resultado[4])
      self.ui.lblnombre.setText(resultado[5])
      self.ui.btnValidar.setEnabled(True)
      self.ui.entRuc.setEnabled(False)
      self.ui.entSol.setEnabled(False)
      self.ui.entToken.setEnabled(False)
      self.ui.lblnombre.setEnabled(False)
      self.ui.btnSelect.setEnabled(False)
    else:
      self.ui.entRuc.setText("")
      self.ui.entSol.setText("")
      self.ui.entToken.setText("")
      self.ui.lblnombre.setText("No se ha seleccionado ninguna carpeta")
      self.ui.btnValidar.setEnabled(False)
      self.ui.entRuc.setEnabled(True)
      self.ui.entSol.setEnabled(True)
      self.ui.entToken.setEnabled(True)
      self.ui.lblnombre.setEnabled(True)
      self.ui.btnSelect.setEnabled(True)
  def validar(self):
    path = self.ui.lblnombre.text()
    ruc = self.ui.entRuc.text()
    client_id = self.ui.entSol.text()
    client_secret = self.ui.entToken.text()
    periodo = self.ui.cbMes.currentText()+self.ui.cbAnio.currentText()
    text_files = [f for f in os.listdir(path) if f.endswith('.dbf')]
    if 'tbregdatos.dbf' in text_files:
      token = self.Mtos.getToken(client_id,client_secret).json()
      if 'access_token' in token:
        try:
          lista = [token['access_token'],ruc,path,periodo]
          tabla = Tabla(parent=self,listInfo=lista)
          tabla.setModal(True)
          tabla.show()
          tabla.exec_()
          tabla.close()
        except Exception as e:
          self.error(f"Verifique el periodo {periodo} o el archivo 'tbregdatos.dbf \n Error: {e}")
      else:
        self.error("Error en la autenticación, verifique que los datos coinciden")
    else:
      self.error("La carpeta no contiene el archivo 'tbregdatos.dbf'")
  def error(self,msg):
    nuevo = QErrorMessage(self)
    nuevo.setModal(True)
    nuevo.showMessage(msg)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = Principal()
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
