import sqlite3

class Data:
    
    def __init__(self):
        # Conectar a la base de datos (o crearla si no existe)
        self.conn = sqlite3.connect('D:/Desarrollos Python/Petinatti-Control-Bulto/controlbulto/src/controlbulto/db.sqlite3')
        # Crear un cursor para interactuar con la base de datos
        self.cursor = self.conn.cursor()
	
    def insert(self):
        # Insertar datos en la tabla
        cursor.execute('''INSERT INTO usuarios (nombre, edad) VALUES (?, ?)''', ('Juan', 30))
        # Guardar (confirmar) los cambios
        conexion.commit()

    def select(self):
        # Consultar datos
        self.cursor.execute('SELECT * FROM Bultos')
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        self.conexion.close()
        return filas
    
    def select_SSCC(self, sscc):
        # Consultar datos
        self.cursor.execute("SELECT ItemCode, ItemDescription, Quantity FROM Bultos Where SSCC = '" + str(sscc) + "'")
        filas = self.cursor.fetchall()
        # for fila in filas:
        #    print(fila)       
        # Cerrar la conexión
        self.conn.close()
        return filas




'''
d = Data()		
items = d.select_SSCC('000000000003839844')
for i in items:
	print(i)
'''