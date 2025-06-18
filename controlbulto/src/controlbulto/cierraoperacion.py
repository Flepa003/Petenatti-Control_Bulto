from controlbulto.database_hana import *

class CierraBultos():
    
    def cierra(self):

        if (self.totalBultos_input.value != ''):
            if (self.totalBultos_input.value == len(self.sscc_controlados)):
                # Impacto la Marca en la tabla LUID con los bultos OK
                for ok_bultos in self.sscc_controlados:
                    self.db.cierraPREPARADOS(ok_bultos,self.user_name)
            else:
                ask_a_question = toga.InfoDialog('Advertencia!','NO coincide la cantidad de Bultos reportados...')
                if await self.main_window.dialog(ask_a_question):
                    print("OK!")
        else:
            ask_a_question = toga.InfoDialog('Advertencia!','Bultos Total en blanco...')
            if await self.main_window.dialog(ask_a_question):
                print("OK!")