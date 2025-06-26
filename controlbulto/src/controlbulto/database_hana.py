# import sqlite3
import os
import configparser
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
        # Leer configuraciones
        config = configparser.ConfigParser()
        # Obtener la ruta del archivo en la carpeta actual
        current_directory = os.getcwd()
        # current_directory = "D:\Desarrollos Python\Petinatti-Control-Bulto\controlbulto"
        config_file_path = os.path.join(current_directory, 'settings.ini')
        # print(config_file_path)

        # Leer el archivo de configuración
        config.read(config_file_path)

        # Acceder a configuraciones
        self.entorno = config.get("general", "entorno")
        self.database = config.get("general", "database")
        # PARA PRUEBAS
        # self.database = "SBOPHNOTST"
        # print(f"ENTORNO: {self.entorno}")
        # Tomo los valores de la DB con la cual trabajar


	
    def insert(self):
        # Insertar datos en la tabla
        self.cursor.execute('''INSERT INTO usuarios (nombre, edad) VALUES (?, ?)''', ('Juan', 30))
        # Guardar (confirmar) los cambios
        self.conexion.commit()

    def select(self):
        # Consultar datos
        # self.cursor.execute('SELECT * FROM SBOPHNOTST.PMX_SSCC_SHIPPING_LABEL Where "BARCODE" is not null')
        # PRODUCCION
        self.cursor.execute('SELECT * FROM ' + str(self.database) + '."PMX_SSCC_SHIPPING_LABEL" Where "BARCODE" is not null')
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        self.conexion.close()
        return filas
    
    def select_SSCC_OLA(self, muelle, ola):
        # Consultar datos
        # self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity" FROM "SBOPHNOTST"."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND "SSCC" = ' +"'" + str(sscc) + "'")
        # PRODUCCION
        # self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity" FROM ' + str(self.database) + '."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND "SSCC" = ' +"'" + str(sscc) + "'")
        self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity", "SSCC" FROM ' + str(self.database) + '."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND  "DestStorLocCode" = ' + "'" + str(muelle) + "'" + '	AND "Ola" = ' + "'" + str(ola) + "'")
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        # self.conn.close()
        return filas    
    
    def select_SSCC(self, sscc, muelle, ola):
        # Consultar datos
        # self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity" FROM "SBOPHNOTST"."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND "SSCC" = ' +"'" + str(sscc) + "'")
        # PRODUCCION
        # self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity" FROM ' + str(self.database) + '."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND "SSCC" = ' +"'" + str(sscc) + "'")
        self.cursor.execute('SELECT "ItemCode", "PRODUCTDESCRIPTION", "Quantity", "SSCC" FROM ' + str(self.database) + '."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' AND  "DestStorLocCode" = ' + "'" + str(muelle) + "'" + '	AND "Ola" = ' + "'" + str(ola) + "'" + ' AND "SSCC" = ' + "'" + str(sscc) + "'")
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
        self.cursor.execute('Select Distinct "DestStorLocCode" From ' + str(self.database) + '."PMX_SSCC_SHIPPING_READY_ARG"  Order By "DestStorLocCode" ')
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        # self.conn.close()
        return filas

    def select_OLA(self):
        # Consultar datos
        # self.cursor.execute('Select Distinct "DestStorLocCode" From "SBOPHNOTST"."PMX_SSCC_SHIPPING_READY_ARG"  Order By "DestStorLocCode" ')
        # PRODUCCION
        self.cursor.execute('Select Distinct "DestStorLocCode" , "Ola" From ' + str(self.database) + '."PMX_SSCC_SHIPPING_READY_ARG" Where "ARG_PROCESS" = ' + "'N'" + ' Order By "DestStorLocCode" , "Ola" ')
        filas = self.cursor.fetchall()
        muelle_ola = []
        for fila in filas:
            muelle_ola.append(fila[0] + '-' + str(fila[1]))
        #    print(muelle_ola)       
        # Cerrar la conexión
        # self.conn.close()
        # return filas
        return muelle_ola


    def select_Bulto(self, ref):
        # Consultar datos
        # self.cursor.execute("SELECT * FROM SBOPHNOTST.PMX_SSCC_SHIPPING_READY_ARG Where SSCC = '{}' AND Barcode = '{}'".format(ref[0], ref[1]))
        # PRODUCCION
        # PFZ - 20-06-2025: se modifica pues puede existir distintos BarCode para una mismo ItemCode
        # self.cursor.execute("SELECT * FROM " + str(self.database) + ".PMX_SSCC_SHIPPING_READY_ARG Where SSCC = '{}' AND Barcode = '{}'".format(ref[0], ref[1]))
        self.cursor.execute(('Select * From '  + str(self.database) + '.OBCD Where "ItemCode" = ' + "'" + '{}' + "'").format(ref[0][0]))
        filas = self.cursor.fetchall()
        return filas


    def cierraPREPARADOS(self, element, usuario):
		# Actualizo Bulto
        # sql = 'Update "SBOPHNOTST"."PMX_LUID" Set "ARG_PROCESS" = ' + "'Y'" + ', "ARG_FECHACONTROL" = ' + "'" + str(datetime.datetime.now())[0:19]+ "'" + ', "ARG_USER" = ' + "'" + str(usuario) + "'" + ' Where "SSCC" = ' + "'" + str(element) + "'"   
        # PRODUCCION
        sql = 'Update ' + str(self.database) + '."PMX_LUID" Set "ARG_PROCESS" = ' + "'Y'" + ', "ARG_FECHACONTROL" = ' + "'" + str(datetime.datetime.now())[0:19]+ "'" + ', "ARG_USER" = ' + "'" + str(usuario) + "'" + ' Where "SSCC" = ' + "'" + str(element) + "'"   
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