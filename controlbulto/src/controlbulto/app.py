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
        image_path = 'resources/petenatti.png'
        image = toga.Image(image_path)

        # Crear un widget de imagen
        self.image_view = toga.ImageView(image, style=Pack(width=300, height=100))
        
        # Crear los widgets
        self.username_input = toga.TextInput(placeholder='Usuario')
        self.password_input = toga.PasswordInput(placeholder='Contraseña')
        self.login_button = toga.Button('Iniciar Sesión', on_press=self.login, style=Pack(flex=1,background_color='#4F8DD9', height=30))

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
        
        # session_id = login_to_sap_b1("SBOPHNOTST",username, password)
        # PRODUCCION
        # session_id = login_to_sap_b1("PETHNOPROD",username, password)
        session_id = 'OK'
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
        self.muelle_label = toga.Label("MUELLE - OLA",style=Pack(padding=(15,125), font_weight=BOLD, background_color='#56a050', height=20, alignment=CENTER ))                       
        self.muelle_button_back = toga.Button('Anterior', on_press=self.atras_0, style=Pack(flex=1, height=40))
        # Conecto a Hana
        self.db = Data()
        #
        # self.muelle_filas = self.db.select_MUELLE()
        self.muelle_filas = self.db.select_OLA()
        #
        self.muelle_selection = toga.Selection(
            items=self.muelle_filas, on_change=self.proceso,
            style=Pack(padding=(0, 5))
        )
        #
        # Añadir los widgets al contenedor
        self.muelle_box.add(self.muelle_label)
        self.muelle_box.add(self.muelle_selection)
        self.muelle_box.add(self.muelle_button_back)
        # Añadir el contenedor a la ventana principal
        self.main_window.content = self.muelle_box
        self.main_window.show()

            
    def proceso(self, widget):
        # Tomo Muelle y Ola
        indice = str(widget.value).find("-")
        # Guardo el muelle
        self.muelle = str(widget.value)[:indice]
        # Guardo el Ola
        self.ola = str(widget.value)[indice+1:]

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
        self.name_label_muelle = toga.Label(self.muelle + ' - ' + self.ola,style=Pack(padding=(15,160), font_weight=BOLD, background_color='#56a050', height=15, alignment=CENTER ))
        #
        self.main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))
        self.label_name_box = toga.Box(style=Pack(direction=COLUMN, padding=5, background_color=ORANGE))
        self.name_label = toga.Label("SSCC",style=Pack(padding=(15,160), font_weight=BOLD, background_color=ORANGE, height=20, alignment=CENTER ))
        #
        self.label_name_box.add(self.name_label)
        #        
        self.name_input = toga.TextInput(on_confirm=self.scan_SSCC,style=Pack(flex=1))
        name_button_back = toga.Button('Anterior', on_press=self.atras_1, style=Pack(flex=1))
        self.name_button_cierre = toga.Button('Cerrar SSCC', on_press=self.cerrar, style=Pack(flex=1, background_color='#38a310'))
        self.action_name_box = toga.Box(children=[name_button_back, self.name_button_cierre],
                                   style=Pack(flex=1, direction=ROW),
        )

        self.name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        # self.name_box.add(self.image_view)
        #
        self.muelle_box.add(self.name_label_muelle)
        #
        self.name_box.add(self.label_name_box)
        self.name_box.add(self.name_input)
        self.name_box.add(self.action_name_box)


        self.main_box.add(self.muelle_box)
        self.main_box.add(self.name_box)

        # self.main_window = toga.MainWindow(title=self.formal_name, size=(300, 300))
        self.main_window.content = self.main_box
        self.name_input.focus()
        self.main_window.show()

    async def scan_SSCC(self, widget):
        #if(self.p_ini == 1):
        self.name_box.remove(self.action_name_box)
        #
        self.resul_box_box = toga.Box()
        self.resul_box_box.style = Pack(direction=COLUMN, padding=10)
        # Crear una tabla para mostrar los resultados
        self.table = toga.Table(
            headings=['Item','Description','Qty'],
                style=Pack(flex=1)
        )
        # Valido si este SSCC ya fue scaneado
        if(len(self.sscc_controlados) > 0):
            if(widget.value in self.sscc_controlados):
                # Ya fue scaneado el SSCC
                ask_a_question = toga.InfoDialog("ADVERTENCIA!", "SSCC ya scaneado...")
                if await self.main_window.dialog(ask_a_question):
                    print("The user said yes!")
                self.name_input.value = ''
                return
            else:
                # Guardo el SSCC para uso posterior
                self.mySSCC = widget.value
        else:
            # Guardo el SSCC para uso posterior
            self.mySSCC = widget.value
        # Controlo el largo del SSCC a 18
        if (len(self.mySSCC) > 18):
            self.mySSCC = self.mySSCC[-18:]
        # Busco los datos en la DB
        self.filas = self.db.select_SSCC(self.mySSCC, self.muelle, self.ola)
        # Valido la existencia del SSCC
        if(len(self.filas) == 0):
            # self.main_window.error_dialog('ERROR...','SSCC NO ENCONTRADO...\nSSCC YA CONTROLADO...')
            ask_a_question = toga.InfoDialog("ERROR!", "SSCC inexistente...")
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
        # Busco la Cantidad de SSCC por OLA
        self.cantidad_sscc_ola = self.db.select_SSCC_OLA(self.muelle,self.ola)
        self.label_qty_sscc = toga.Label('SSCC restantes: ' + str(len(self.cantidad_sscc_ola) - len(self.sscc_controlados)) + ' de ' + str(len(self.cantidad_sscc_ola)) + ', para Ola: ' + str(self.ola) )
        # Agrego los items para mostrar al box
        self.resul_box_box.add(self.label_qty_sscc)
        self.resul_box_box.add(self.table)
        self.resul_box_box.add(self.bultoId_box)
      
        # Buttons
        btn_style = Pack(flex=1)
        btn_app_back = toga.Button("Anterior", on_press=self.button_cancelar, style=btn_style)
        btn_app_cancelar = toga.Button("Cancelar", on_press=self.atras_1, style=Pack(flex=1, background_color='#F86969'))
        # btn_app_back = toga.Button("Cerrar Control", on_press=self.button_cancelar, style=Pack(flex=1, background_color='#38a310'))
        # Outermost box
        self.action_box = toga.Box(children=[btn_app_back, btn_app_cancelar],
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
        myMSG = False
        global mensaje
        mensaje = toga.Label('', style=Pack(padding=(10), color='red'))           
        # Creo la lista de SSCC + Barcode
        myElement = [self.mySSCC, widget.value]
        bulto = self.db.select_Bulto(self.filas)
        if (len(bulto) > 0):
            # mensaje
            #self.main_window.info_dialog('Bulto','Id scan Ok!')
            # Verifico que los Items coincidan
            for barcodes in bulto:
                if(widget.value == barcodes[1]):
                    # Agrego los butos para su impacto/cancelacion
                    if len(self.bultos_controlados) == 0:
                        self.sscc_controlados=[self.mySSCC]
                        self.bultos_controlados= [widget.value]
                    else:
                        # Debo verificar si el Bulto ya fue scaneado
                        self.sscc_controlados.append(self.mySSCC)
                        self.bultos_controlados.append(widget.value)
                    myMSG = False
                    break
                else:
                    myMSG = True
            #        
            if(myMSG):
                ask_a_question = toga.InfoDialog('ERROR...','El Barcode NO corresponde con el Item del SSCC...')
                if await self.main_window.dialog(ask_a_question):
                    print("No ENCONTRADO!")            
        else:
            # mensaje = toga.Label('ERROR: id NO ENCONTRADO!', style=Pack(padding=(10,10), color='red'))
            ask_a_question = toga.InfoDialog('ERROR...','Barcode NO ENCONTRADO...')
            if await self.main_window.dialog(ask_a_question):
                print("No ENCONTRADO!")
            myMSG = True
        # Añadir el mensaje a la caja principal
        # print(f"SSCC scaneados: {self.sscc_controlados}")
        # print(f"Bultos scaneados: {self.bultos_controlados}")
        widget.value = ''      
        # Pop-Up con mensaje en medio de la pantalla 
        if(myMSG):
            # Me quedo en el mismo bultos a la espera de un proximo scan valido
            myMSG = False
        elif((len(self.cantidad_sscc_ola) - len(self.sscc_controlados)) == 0):
            # Cierror el SSCC
            self.name_input.value = ''
            self.main_window.content.remove(self.resul_box_box)
            self.cerrar(widget)
        else:
            # Continuo controlando los butlos 
            self.proximoBulto(widget)
        # return
            
    
    def proximoBulto(self, widget):
        # Limpio y scaneo el proximo
        self.name_input.value = ''
        self.main_window.content.remove(self.resul_box_box)
        self.name_box.add(self.action_name_box)
        self.name_input.focus()
    
    
    
    
    def cerrar(self, widget):
        # Procedimiento para cierre del SSCC
        async def opera_cierre(widget):
            # Controlo los totales
            print(f"Cantidad de SSCC: {len(self.sscc_controlados)}" )
            if (totalBultos_input.value != ''):
                print(f"Total de Bultos ingresado por pantalla: {totalBultos_input.value}" )
                if (totalBultos_input.value == str(len(self.sscc_controlados))):
                    # Impacto la Marca en la tabla LUID con los bultos OK
                    for ok_bultos in self.sscc_controlados:
                        self.db.cierraPREPARADOS(ok_bultos,self.user_name)
                else:
                    ask_a_question = toga.InfoDialog('Advertencia!','NO coincide la cantidad de Bultos reportados...')
                    if await self.main_window.dialog(ask_a_question):
                        print("OK!")
                    return
            else:
                ask_a_question = toga.InfoDialog('Advertencia!','Bultos Total en blanco...')
                if await self.main_window.dialog(ask_a_question):
                    print("OK!")
                return
            self.sscc_controlados.clear()
            self.bultos_controlados.clear()
            self.name_box.remove(self.cierre_box)
            self.seleccionaMuelle()
        # Inhabilito el boton
        self.name_button_cierre.enabled = False
        # Solicito el Total de Bultos con un nuevo box
        totalBultos_input = toga.TextInput(placeholder='Total de Bultos: ',style=Pack(flex=1))
        c_btn_style = Pack(flex=1)
        c_btn_app_confirma = toga.Button("Confirmar", on_press=opera_cierre, style=c_btn_style)
        c_btn_app_cancela = toga.Button("Cancelar", on_press=self.atras_1, style=c_btn_style)
        self.cierre_box = toga.Box(children=[totalBultos_input, c_btn_app_confirma, c_btn_app_cancela],
            style=Pack(flex=1, direction=ROW, padding=20),
        )
        self.name_box.add(self.cierre_box)
        totalBultos_input.focus()



        
    
    def button_cancelar(self,widget):
        # Limpio el control de los bultos
        # self.sscc_controlados.clear()
        # self.bultos_controlados.clear()
        # print('OK! Boton CANCELAR')
        # Retomo al scan del SSCC
        self.name_input.value = ''
        self.main_window.content.remove(self.resul_box_box)
        self.name_box.add(self.action_box)
        self.name_input.focus()
        
    def atras_0(self, widget):
        # self.main_window.error_dialog('ATRAS','Atras...')
        # Limpio la pantalla de Login
        self.main_window.content.remove(self.muelle_box)
        self.main_window.content = self.box_login

    def atras_1(self, widget):
        # self.main_window.error_dialog('ATRAS','Atras...')
        # Limpio la pantalla de Login
        self.main_window.content.remove(self.name_box)
        # self.main_window.content = self.muelle_box
        self.sscc_controlados.clear()
        self.bultos_controlados.clear()
        self.seleccionaMuelle()

    def atras_2(self, widget):
        # self.main_window.error_dialog('ATRAS','Atras...')
        # Limpio la pantalla de Login
        self.main_window.content.remove(self.resul_box_box)
        self.main_window.content.remove(self.name_box)
        # self.main_window.content = self.muelle_box
        self.seleccionaMuelle()


    def salir(self, widget):
        self.main_window.error_dialog('ERROR...','No s epudo conectar a la Base de Datos...')



def main():
    return ControlBulto(formal_name='CONTROL DE BULTO',
                 app_id='pfz-20250310',
                 app_name='ControlBulto',
                 icon='resources/controlbulto.ico')
