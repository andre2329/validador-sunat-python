from PySide2.QtWidgets import QTableWidgetItem
from sqlite3 import connect
import requests
from geopandas import read_file
import pandas as pd
import time
import xlwt
class Metodos():
    def __init__(self):
        super(Metodos,self).__init__()
        self.db_name = 'validador.db'
    def run_query(self, query, parameter=()):
      try:
          with connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameter)
            result = cursor.fetchall()
            conn.commit()
          return result
      except IndexError as e:
        print(e)
      finally:
        conn.close()
    def printOnTable(self,tablewidget:object,lista:list,result:list):
      tablewidget.setColumnCount(len(result[0]))
      tablewidget.setRowCount(len(result))
      tablewidget.setHorizontalHeaderLabels(lista)
      for row in range(len(result)):
        for column in range(len(result[row])):
          tablewidget.setItem(row,column,QTableWidgetItem(str(result[row][column])))
    def reqAndPrint(self,tablewidget:object,headers:list,result:list,token:str,rucPrincipal:str):
      
      tablewidget.setRowCount(len(result))
      headers.insert(-1,'CONSULTA')
      headers.insert(-1,'ESTADO_COMPROBANTE')
      headers.insert(-1,'ESTADO_CONTRIBUYENTE')
      headers.insert(-1,'COND_DOM_CONTRIBUYENTE')
      headers.insert(-1,'Observaciones')
      tablewidget.setColumnCount(len(headers))
      tablewidget.setHorizontalHeaderLabels(headers)
      dicEstadoCp = {"0": "NO EXISTE","1" : "ACEPTADO","2" : "ANULADO","3" :"AUTORIZADO","4" : "NO AUTORIZADO"}
      dicEstadoRuc = {"00" : "ACTIVO","01" : "BAJA PROVISIONAL","02" : "BAJA PROV. POR OFICIO", "03" : "SUSPENSION TEMPORAL", "10" : "BAJA DEFINITIVA","11" : "BAJA DE OFICIO","22" : "INHABILITADO-VENT.UNICA"}
      dicCondDom = {"00" : "HABIDO","09" : "PENDIENTE", "11" : "POR VERIFICAR", "12" : "NO HABIDO", "20" : "NO HALLADO"}
      for row in range(len(result)):
    #['RUC_EMPR','COD_OPER','SER_DOCU','NUM_DOCU','FCH_EMIS','IMP_MONA','IMP_MOEX','REG_CONT','MES_ANO']
        ruc = result[row][0]
        codComp = result[row][1]
        numeroSerie = result[row][2]
        numero = result[row][3]
        fechaEmision = result[row][4]
        montoNa = result[row][5]
        montoEx = result[row][6]
        if (int(result[row][5])==0):
          monto = result[row][6]
        else:
          monto = result[row][5]
        if(codComp == "01" or codComp == "03" or codComp == "08" or codComp == "04" or codComp == "23"):
          validar = True
        elif(codComp == "02"):
          validar = True
          codComp = 'R1'
          if(int(monto)<0):
            codComp = 'R7'
        elif(codComp == "07"):
          validar = True
          monto = str(int(monto*(-1)))
        else:
          validar = False
        if(validar):
          if(numeroSerie[0].isnumeric()):
            monto = ''
          fecha =   result[row][4].split('-')
        #payload = '{'+f'"numRuc":"codComp":"numeroSerie":"numero":"fechaEmision":"monto"
          params = [ruc,codComp,numeroSerie,numero,f'{fecha[2]}/{fecha[1]}/{fecha[0]}',monto]
          resp=self.valida(rucPrincipal,params,token).json()
          if 'success' in resp:
            if resp['success']:
              s = f'Validado - {resp["message"]}'
              result[row].insert(-1,s)
              if 'estadoCp' in resp['data']:
                ind=resp['data']['estadoCp']
                result[row].insert(-1,dicEstadoCp[ind])
              else:
                result[row].insert(-1,'')
              if 'estadoRuc' in resp['data']:
                ind=resp['data']['estadoRuc']
                result[row].insert(-1,dicEstadoRuc[ind])
              else:
                result[row].insert(-1,'')
              if 'condDomiRuc' in resp['data']:
                ind=resp['data']['condDomiRuc']
                result[row].insert(-1,dicCondDom[ind])
              else:
                result[row].insert(-1,'')
              if 'observaciones' in resp['data']:
                result[row].insert(-1,resp['data']['observaciones'])
              else:
                result[row].insert(-1,'')
            else:
              s = 'No se pudo validar - '+ str(resp['message'])
              result[row].insert(-1,s)
          else:
            result[row].insert(-1,'Error en la validacion')
          result[row][-1]=resp
        for column in range(len(result[row])):
          tablewidget.setItem(row,column,QTableWidgetItem(str(result[row][column])))
      tablewidget.resizeColumnsToContents()
    def generarHeaders(self,table:str):
      labels = self.run_query('select name from pragma_table_info(?)',(table,))
      lista = [i[0] for i in labels]
      return lista
    def addRegistro(self,tablename:str,values:tuple):
        count = ',?'*len(values)
        query = f'insert into {tablename} values(null{count})'
        self.run_query(query,values)
    def updRegistro(self,tablename:str,id:int,values:tuple):
        fields = "=?,".join([i for i in self.generarHeaders(tablename) if i != 'ID'])
        query = f'update {tablename} set {fields}=? where id = {id}'
        self.run_query(query,values)
    def delRegistro(self,tablename:str,values:tuple):
        query = f'delete from {tablename} where id = ?'
        self.run_query(query,values)
    def getToken(self,client_id:str,client_secret:str):
      url = f"https://api-seguridad.sunat.gob.pe/v1/clientesextranet/{client_id}/oauth2/token/"
      payload = f'grant_type=client_credentials&scope=https%3A//api.sunat.gob.pe/v1/contribuyente/contribuyentes&client_id={client_id}&client_secret={client_secret}'
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
      response = requests.request("POST", url, headers=headers, data = payload)
      return response
    def valida(self,ruc:str,params:list,token:str):
      url = f"https://api.sunat.gob.pe/v1/contribuyente/contribuyentes/{ruc}/validarcomprobante"
      payload = '{'+f'"numRuc":"{params[0]}","codComp":"{params[1]}","numeroSerie":"{params[2]}","numero":"{params[3]}","fechaEmision":"{params[4]}","monto":"{params[5]}"'+'}'
      headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data = payload)
      return response
    def readDBF(self,path):
      tablaraw = read_file(path)
      tabla = pd.DataFrame(tablaraw)
      return tabla
    def getColumns(self,table,names):
        df = table[names]
        return df
    def selectBy(self,df,column,string):
        return (df[df[column].str.contains(string,case=False)])
    def saveXLSX(self,df,path):
        try:
            df.to_excel(path, index = False)
            return True
        except:
            return False
    def savetoXLS(self, filename:str,tableWidget,original):
      wbk = xlwt.Workbook()
      sheet = wbk.add_sheet("Resultados Sunat", cell_overwrite_ok=True)
      labels = []
      for c in range(tableWidget.columnCount()):
          it = tableWidget.horizontalHeaderItem(c)
          labels.append(str(c+1) if it is None else it.text())
      for i,header in enumerate(labels):
        sheet.write(0,i,header)
      for currentColumn in range(tableWidget.columnCount()):
        for currentRow in range(tableWidget.rowCount()):
          try:
            teext = str(tableWidget.item(currentRow, currentColumn).text())
            sheet.write(currentRow+1, currentColumn,teext)
          except AttributeError:
            pass
      
      sheetOriginal = wbk.add_sheet("Original Extraido", cell_overwrite_ok=True)
      for i,header in enumerate(list(original)[:-1]):
        sheetOriginal.write(0,i,header)
      enLista = original.values.tolist()
      for row in range(len(enLista)):
        for column in range(len(enLista[row][:-1])):
          sheetOriginal.write(row+1,column,str(enLista[row][column]))

      wbk.save(filename)
