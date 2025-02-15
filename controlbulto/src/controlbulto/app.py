"""
Realiza el control del bulto - PMX
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
#
from controlbulto.database import *

class ControlBulto(toga.App):
    def startup(self):
        # Defino el acceso a la DB
        self.db = Data()
        # Creo las pantalla/ventanas
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        self.name_label = toga.Label(
            "Ingrese SSCC: ",
            style=Pack(padding=(0, 5)),
        )
        
        self.name_input = toga.TextInput(on_confirm=self.scan_SSCC,style=Pack(flex=1))

        self.name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.name_box.add(self.name_label)
        self.name_box.add(self.name_input)

        self.main_box.add(self.name_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def scan_SSCC(self, widget):
        self.resul_box_box = toga.Box()
        self.resul_box_box.style = Pack(direction=ROW, padding=10)
        # Crear una tabla para mostrar los resultados
        self.table = toga.Table(
            headings=['ItemCode', 'ItemDescription', 'Qunatity'],
            style=Pack(flex=1)
        )
        # Busco los datos en la DB
        filas = self.db.select_SSCC(widget.value)
        # Mostrar el resultado del query
        # Agregar los resultados a la tabla
        for row in filas:
            self.table.data.append(row)

        # Agrego boton para scan bulto-id
        self.bultoId_label = toga.Label(
            "Bulto-ID: ",
            style=Pack(padding=(0, 5)),
        )
        self.bultoId_input = toga.TextInput(on_confirm=self.validacion,style=Pack(flex=1))
        self.bultoId_box = toga.Box(style=Pack(direction=ROW, padding=5))
        #
        self.bultoId_box.add(self.bultoId_label)
        self.bultoId_box.add(self.bultoId_input)
        #
        # self.resul_box_box.add(self.resul_label)
        self.resul_box_box.add(self.table)
        self.main_box.add(self.resul_box_box)
        self.main_box.add(self.bultoId_box)
        # Inhbailito el boton Scan
        self.main_window.show()
        

    def validacion(self, widget):
        bulto = self.db.select_SSCC(widget.value)
        if (len(bulto) > 0):
            self.terminOK(widget)
        else:
            self.bultoError(widget)
        widget.value = ''
        # Pop-Up con mensaje en medio de la pantalla 



    async def terminOK(self, widget):
        await self.main_window.dialog(
            toga.InfoDialog(
            f"Control Bulto",
            "Finalizado Bye!",
            )
        )
        # widget.value = ''
       
    async def bultoError(self, widget):
        await self.main_window.dialog(
            toga.InfoDialog(
            f"Control Bulto",
            "Bulto-ID NO ENCONTRADO!",
            )
        )
        # widget.value = ''
       


def main():
    return ControlBulto()
