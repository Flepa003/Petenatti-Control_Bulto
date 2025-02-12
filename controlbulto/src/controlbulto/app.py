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
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        self.name_label = toga.Label(
            "Ingrese SSCC: ",
            style=Pack(padding=(0, 5)),
        )
        
        self.name_input = toga.TextInput(style=Pack(flex=1))

        self.name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.name_box.add(self.name_label)
        self.name_box.add(self.name_input)

        self.button = toga.Button(
            "SCAN",
            on_press=self.scan_SSCC,
            style=Pack(padding=15),
        )

        self.main_box.add(self.name_box)
        self.main_box.add(self.button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def scan_SSCC(self, sender):
        self.resul_box_box = toga.Box()
        self.resul_box_box.style = Pack(direction=ROW, padding=10)
        # Crear una tabla para mostrar los resultados
        self.table = toga.Table(
            headings=['ItemCode', 'ItemDescription', 'Qunatity'],
            style=Pack(flex=1)
        )
        # Busco los datos en la DB
        # d = Data()
        # filas = d.select_SSCC(self.name_input.value)
        # Mostrar el resultado del query
        # Agregar los resultados a la tabla
        #for row in filas:
        #    self.table.data.append(row)
        #       self.resul_label.text = str(filas)       
        new_row0 = ('A0120200242', 'Formitas De Pollo Rebozadas Nuggets Congeladas Calisa (5 KG.)', 2)
        self.table.data.append(new_row0)
        new_row1 = ('A0120200242', 'Formitas De Pollo Rebozadas Nuggets Congeladas Calisa (5 KG.)', 9)
        self.table.data.append(new_row1)
        new_row2 = ('A0330200601', 'Brocoli Congelado Iqf Conosud (1 KG.)', 1)
        self.table.data.append(new_row2)
        
        # Agrego boton para scan bulto-id
        self.bultoId_label = toga.Label(
            "Bulto-ID: ",
            style=Pack(padding=(0, 5)),
        )
        self.bultoId_input = toga.TextInput(style=Pack(flex=1))
        self.bultoId_box = toga.Box(style=Pack(direction=ROW, padding=5))
        #
        self.bultoId_box.add(self.bultoId_label)
        self.bultoId_box.add(self.bultoId_input)
        #
        self.button2 = toga.Button(
            "SCAN Bulto ID",
            on_press=self.terminOK,
            style=Pack(padding=15),
        )

        # self.resul_box_box.add(self.resul_label)
        self.resul_box_box.add(self.table)
        self.main_box.add(self.resul_box_box)
        self.main_box.add(self.bultoId_box)
        self.main_box.add(self.button2)
        # Inhbailito el boton Scan
        self.button.enabled = False
        self.main_window.show()
     
    # def terminOK(self, sender):
    #    print('OK!')
    # Pop-Up con mensaje en medio de la pantalla 
    async def terminOK(self, widget):
        await self.main_window.dialog(
            toga.InfoDialog(
            f"Control Bulto",
            "Finalizado Bye!",
            )
        )   


def main():
    return ControlBulto()
