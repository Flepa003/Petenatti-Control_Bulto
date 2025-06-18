# import sqlite3
import datetime
from hdbcli import dbapi

class Data:
    
    def __init__(self):
        # Conectar a la base de datos (o crearla si no existe)
        # self.conn = sqlite3.connect('D:/Desarrollos Python/Petinatti-Control-Bulto/controlbulto/src/controlbulto/db.sqlite3')
        #Initialize your connection
        self.conn = dbapi.connect(
    		address='192.168.220.161',
    		port='30015',
    		user='SYSTEM',
    		password='!!PetAdm1n'
		)
        # Crear un cursor para interactuar con la base de datos
        # try:
        self.cursor = self.conn.cursor()
        # except Exception as e:
            # Captura cualquier excepción y la imprime
            # print(f"Ha ocurrido un error: {e}")

	
    def insert(self):
        # Insertar datos en la tabla
        cursor.execute('''INSERT INTO usuarios (nombre, edad) VALUES (?, ?)''', ('Juan', 30))
        # Guardar (confirmar) los cambios
        conexion.commit()

    def select(self):
        # Consultar datos
        # self.cursor.execute('SELECT * FROM SBOPHNOTST.PMX_SSCC_SHIPPING_LABEL Where "BARCODE" is not null')
        # PRODUCCION
        self.cursor.execute('SELECT * FROM PETHNOPROD.PMX_SSCC_SHIPPING_LABEL Where "BARCODE" is not null')
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        self.conexion.close()
        return filas
    
    def select_SSCC(self, sscc):
        # Consultar datos
        # self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity" FROM "SBOPHNOTST"."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND "SSCC" = ' +"'" + str(sscc) + "'")
        # PRODUCCION
        self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity" FROM "PETHNOPROD"."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND "SSCC" = ' +"'" + str(sscc) + "'")
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        # self.conn.close()
        return filas

    def select_MUELLE(self):
        # Consultar datos
        # self.cursor.execute('Select Distinct "DestStorLocCode" From "SBOPHNOTST"."PMX_SSCC_SHIPPING_READY_ARG"  Order By "DestStorLocCode" ')
        # PRODUCCION
        self.cursor.execute('Select Distinct "DestStorLocCode" From "PETHNOPROD"."PMX_SSCC_SHIPPING_READY_ARG"  Order By "DestStorLocCode" ')
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        # self.conn.close()
        return filas


    def select_Bulto(self, ref):
        # Consultar datos
        # self.cursor.execute("SELECT * FROM SBOPHNOTST.PMX_SSCC_SHIPPING_READY_ARG Where SSCC = '{}' AND Barcode = '{}'".format(ref[0], ref[1]))
        # PRODUCCION
        self.cursor.execute("SELECT * FROM PETHNOPROD.PMX_SSCC_SHIPPING_READY_ARG Where SSCC = '{}' AND Barcode = '{}'".format(ref[0], ref[1]))
        filas = self.cursor.fetchall()
        return filas


    def cierraPREPARADOS(self, element, usuario):
		# Actualizo Bulto
        # sql = 'Update "SBOPHNOTST"."PMX_LUID" Set "ARG_PROCESS" = ' + "'Y'" + ', "ARG_FECHACONTROL" = ' + "'" + str(datetime.datetime.now())[0:19]+ "'" + ', "ARG_USER" = ' + "'" + str(usuario) + "'" + ' Where "SSCC" = ' + "'" + str(element) + "'"   
        # PRODUCCION
        sql = 'Update "PETHNOPROD"."PMX_LUID" Set "ARG_PROCESS" = ' + "'Y'" + ', "ARG_FECHACONTROL" = ' + "'" + str(datetime.datetime.now())[0:19]+ "'" + ', "ARG_USER" = ' + "'" + str(usuario) + "'" + ' Where "SSCC" = ' + "'" + str(element) + "'"   
        # print(sql)
		# execute the query
        self.cursor.execute(sql)
        self.conn.commit()		
        


'''
d = Data()		
items = d.select_SSCC('000000000003839844')
for i in items:
	print(i)
'''