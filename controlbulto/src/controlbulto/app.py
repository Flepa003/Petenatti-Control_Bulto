"""
Realiza el control del bulto - PMX
"""
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import BOLD, COLUMN, CENTER, CENTER
from toga.constants import *
#
from controlbulto.database_hana import *
from controlbulto.loginSAP import *


class ControlBulto(toga.App):
    def startup(self):
        # Crear la ventana principal
        self.main_window = toga.MainWindow(title=self.formal_name, size=(300, 300))
        #
        # Cargar la imagen
        image_path = 'resources/icono.png'
        image = toga.Image(image_path)

        # Crear un widget de imagen
        self.image_view = toga.ImageView(image, style=Pack(width=300, height=100))
        
        # Crear los widgets
        self.username_input = toga.TextInput(placeholder='Usuario')
        self.password_input = toga.PasswordInput(placeholder='Contraseña')
        self.login_button = toga.Button('Iniciar Sesión', on_press=self.login, style=Pack(flex=1,background_color='#4F8DD9', height=40))

        # Crear el contenedor principal
        self.box_login = toga.Box(style=Pack(direction=COLUMN, padding=(0,10)))

        # Añadir los widgets al contenedor
        self.box_login.add(self.image_view)
        self.box_login.add(self.username_input)
        self.box_login.add(self.password_input)
        self.box_login.add(self.login_button)
        # Añadir el contenedor a la ventana principal
        self.main_window.content = self.box_login
        self.main_window.show()
        

    def login(self, widget):
        username = self.username_input.value
        password = self.password_input.value
        
        session_id = login_to_sap_b1("SBOPHNOTST",username, password)
        #if username == 'admin' and password == '123':
        if (session_id):
            # self.main_window.info_dialog('Login Exitoso', '¡Bienvenido!')
            # Obtengo usuario para grbar control
            self.user_name = username
            # self.main_window.content.remove(self.box_login)
            # self.main_window.close()
            self.seleccionaMuelle()
            
        else:
            self.main_window.error_dialog('Error de Login', 'Usuario o contraseña incorrectos.')
            self.password_input.focus()
    
    def seleccionaMuelle(self):
        # Limpio la pantalla de Login
        self.main_window.content.remove(self.box_login)
        # Crear los widgets
        self.muelle_box = toga.Box(style=Pack(direction=COLUMN, padding=5, background_color='#56a050', width=300, height=40))
        self.muelle_label = toga.Label("MUELLE",style=Pack(padding=(15,130), font_weight=BOLD, background_color='#56a050', height=20, alignment=CENTER ))                       
        # Conecto a Hana
        self.db = Data()
        #
        self.muelle_filas = self.db.select_MUELLE()
        #
        self.muelle_selection = toga.Selection(
            items=self.muelle_filas, on_change=self.proceso,
            style=Pack(padding=(0, 5))
        )
        #
        # Añadir los widgets al contenedor
        self.muelle_box.add(self.muelle_label)
        self.muelle_box.add(self.muelle_selection)
        # Añadir el contenedor a la ventana principal
        self.main_window.content = self.muelle_box
        self.main_window.show()

            
    def proceso(self, widget):
        # Guardo el muelle
        self.muelle = widget.value
        # Limpio la pantalla de Login
        self.main_window.content.remove(self.muelle_box)
        # Creo seleccion de MUELLE
        # Vble. de control
        self.p_ini = 0
        # Creo la lista para guardar los Bultos controlados OK
        self.sscc_controlados = []
        self.bultos_controlados = []
        # Creo las pantalla/ventanas
        self.muelle_box = toga.Box(style=Pack(direction=COLUMN, padding=5, background_color='#56a050'))
        self.main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

        self.name_label_muelle = toga.Label(self.muelle,style=Pack(padding=(15,160), font_weight=BOLD, background_color='#56a050', height=15, alignment=CENTER ))
        self.name_label = toga.Label("SSCC",style=Pack(padding=(15,160), font_weight=BOLD, background_color=ORANGE, height=20, alignment=CENTER ))
                
        self.name_input = toga.TextInput(on_confirm=self.scan_SSCC,style=Pack(flex=1))

        self.name_box = toga.Box(style=Pack(direction=COLUMN, padding=5, background_color=ORANGE))
        # self.name_box.add(self.image_view)
        self.muelle_box.add(self.name_label_muelle)
        self.name_box.add(self.name_label)
        self.name_box.add(self.name_input)

        self.main_box.add(self.muelle_box)
        self.main_box.add(self.name_box)

        # self.main_window = toga.MainWindow(title=self.formal_name, size=(300, 300))
        self.main_window.content = self.main_box
        self.name_input.focus()
        self.main_window.show()

    async def scan_SSCC(self, widget):
        if(self.p_ini == 1):
            self.main_window.content.remove(self.resul_box_box)
        self.resul_box_box = toga.Box()
        self.resul_box_box.style = Pack(direction=COLUMN, padding=10)
        # Crear una tabla para mostrar los resultados
        self.table = toga.Table(
            headings=['Item','Description','Qty'],
                style=Pack(flex=1)
        )
        # Guardo el SSCC para uso posterior
        self.mySSCC = widget.value
        # Controlo el largo del SSCC a 18
        if (len(self.mySSCC) > 18):
            self.mySSCC = self.mySSCC[-18:]
        # Busco los datos en la DB
        self.filas = self.db.select_SSCC(self.mySSCC)
        # Valido la existencia del SSCC
        if(len(self.filas) == 0):
            # self.main_window.error_dialog('ERROR...','SSCC NO ENCONTRADO...\nSSCC YA CONTROLADO...')
            ask_a_question = toga.InfoDialog("ERROR!", "SSCC NO ENCONTRADO...\nSSCC YA CONTROLADO...")
            if await self.main_window.dialog(ask_a_question):
                print("The user said yes!")
            
            self.name_input.value = ''
            return
        # Guardo la cantidad de filas para la iteracion
        self.cantidad_bultos = len(self.filas)
        # Mostrar el resultado del query
        # Agregar los resultados a la tabla
        for row in self.filas:
            self.table.data.append(row)
        # Agrego boton para scan bulto-id
        self.bultoId_label = toga.Label(
            "BARCODE",
            style=Pack(padding=(15, 140), font_weight=BOLD, background_color='#4F8DD9', height=20, alignment=CENTER ),
        )
        self.bultoId_input = toga.TextInput(on_confirm=self.validacion,style=Pack(flex=1))
        self.bultoId_box = toga.Box(style=Pack(direction=COLUMN, padding=5, background_color='#4F8DD9'))
        #
        self.bultoId_box.add(self.bultoId_label)
        self.bultoId_box.add(self.bultoId_input)
        #
        # self.resul_box_box.add(self.resul_label)
        self.resul_box_box.add(self.table)
        self.resul_box_box.add(self.bultoId_box)
      
        # Buttons
        btn_style = Pack(flex=1)
        btn_app_cerrar = toga.Button("Cerrar Control", on_press=self.button_cerrar, style=btn_style)
        btn_app_cancelar = toga.Button("Cancelar", on_press=self.button_cancelar, style=Pack(flex=1,background_color='#F86969'))
        # Outermost box
        self.action_box = toga.Box(children=[btn_app_cerrar,btn_app_cancelar],
            style=Pack(flex=1, direction=ROW, padding=20),
        )
        self.resul_box_box.add(self.action_box)
        self.main_box.add(self.resul_box_box)
        # Dejop foco en el BultoID
        self.bultoId_input.focus()
        # Actualizo vble
        self.p_ini = 1
        # Inhbailito el boton Scan
        self.main_window.show()
        

    async def validacion(self, widget):
        # Crear un mensaje
        global mensaje
        mensaje = toga.Label('', style=Pack(padding=(10), color='red'))
        # Creo la lista de SSCC + Barcode
        myElement = [self.mySSCC, widget.value]
        bulto = self.db.select_Bulto(myElement)
        if (len(bulto) > 0):
            # mensaje
            #self.main_window.info_dialog('Bulto','Id scan Ok!')
            # Agrego los butos para su impacto/cancelacion
            if len(self.bultos_controlados) == 0:
                self.sscc_controlados=[self.mySSCC]
                self.bultos_controlados= [widget.value]
            else:
                self.sscc_controlados.append(self.mySSCC)
                self.bultos_controlados.append(widget.value)
            
        else:
            # mensaje
            # mensaje = toga.Label('ERROR: id NO ENCONTRADO!', style=Pack(padding=(10,10), color='red'))
            ask_a_question = toga.InfoDialog('ERROR...','Barcode NO ENCONTRADO...')
            if await self.main_window.dialog(ask_a_question):
                print("The user said yes!")
        # Añadir el mensaje a la caja principal
        # self.bultoId_box.add(mensaje)
        widget.value = ''
        
        # Pop-Up con mensaje en medio de la pantalla 
        if(len(self.bultos_controlados) ==  self.cantidad_bultos):
            self.button_cerrar('')
        elif(len(self.bultos_controlados) > 0):
            # Busco el bulto ya scaneado
            resultado = next((tupla for tupla in self.filas if self.bultos_controlados[0] in tupla), None)
            # print(resultado)
            if resultado:
                self.filas.remove(resultado)
                self.table.data.clear()
                for row in self.filas:
                    self.table.data.append(row)
            # return
            
    
    def button_cerrar(self,widget):
        # Impacto la Marca en la tabla LUID con los bultos OK
        for ok_bultos in self.sscc_controlados:
            self.db.cierraPREPARADOS(ok_bultos,self.user_name)
        # print('OK! CERRAR-- REVISAR --')
        # Retomo al scan del SSCC
        self.sscc_controlados.clear()
        self.bultos_controlados.clear()
        self.name_input.value = ''
        self.main_window.content.remove(self.resul_box_box)
        self.name_input.focus()

        
    
    def button_cancelar(self,widget):
        # Limpio el control de los bultos
        self.sscc_controlados.clear()
        self.bultos_controlados.clear()
        # print('OK! Boton CANCELAR')
        # Retomo al scan del SSCC
        self.name_input.value = ''
        self.main_window.content.remove(self.resul_box_box)
        self.name_input.focus()
        
    def salir(self):
        self.main_window.error_dialog('ERROR...','No s epudo conectar a la Base de Datos...')

def main():
    return ControlBulto()
