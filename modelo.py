import sqlite3
import re
from peewee import *
from datetime import datetime
from datetime import datetime
import time
from plyer import notification
import threading
from tkinter import Tk, Label, Button, Toplevel
import threading



db = SqliteDatabase("base_ejemplo.db")


class BaseModel(Model):
    class Meta:
        database = db


class Mensajes(BaseModel):
    
        mensajes = CharField()
        horario = CharField()


db.connect()
db.create_tables([Mensajes])


class operaciones:
    def __init__(self, valor_mensajes, valor_horario):

        self.valor_mensajes = valor_mensajes  # Inicializa las variables
        self.valor_horario = valor_horario
        
        self.iniciar_verificacion()
        

    # Funciones CRUD-------------------------------------------------------------------------
   


    def funcion_alta(self, mensajes, horario, tree):
        texto = mensajes.get().strip()  # Ahora obtendrás el texto del StringVar
        hora = horario.get().strip()
        
        if not texto or not hora:
            return "Error: El mensaje o el Horario estan vacios."

        # Verifica la expresión regular
        expresion = "^[a-zA-ZÀ-ÿ0-9\s]+$"
        if re.match(expresion, texto):
            
                try:
                    datetime.strptime(hora, "%H:%M") 
                except ValueError:
                    return "Error: El horario debe estar en formato HH:MM."

                nuevo_mensaje = Mensajes(mensajes=texto, horario=hora)
                nuevo_mensaje.save()

                self.funcion_actualizar(tree)
                mensajes.set("")  # Limpia el campo después de guardar
                horario.set("")
                return "Registro dado de alta"
        else:
                return "Error: El mensaje no cumple con el formato."



    def funcion_actualizar(self, tree):

        records = tree.get_children()
        for element in records:
            tree.delete(element)
        for fila in Mensajes.select():
            tree.insert(
                "",
                "end",
                text=fila.id,
                values=(
                    fila.mensajes,
                    fila.horario,
                ),
            )

    # ----------------------------------------------------------------------------------------
    
    def funcion_borrar(self, tree):
        seleccion = tree.selection()
        if not seleccion:
            return "No hay ningun registro seleccionado"
        for item_id in seleccion:
            item = tree.item(item_id) #Obtiene contenido del elemento seleccionado
            mi_id = item["text"]
            try: 
                borrar = Mensajes.get(Mensajes.id == mi_id)
                borrar.delete_instance()
            except:
                return f"Error al intentar borrar el registro: {e}"
        
        self.funcion_actualizar(tree)
        
        return "Registro eliminado con exito"

    # ------------------------------------------------------------------------------------------------------------

    def funcion_modificar(
        self,
        mensajes,
        horario,
        tree,
    ):
        cliente = tree.selection()
        item = tree.item(cliente)
        mi_id = item["text"]
        actualizar = Mensajes.update(mensajes=mensajes.get(), horario=horario.get()).where(Mensajes.id == mi_id)
        actualizar.execute() 
        
        self.funcion_actualizar(tree)
        mensajes.set("")
        return "Registro modificado"
    

    def verificar_horario(self):
        while True:
            # Obtén el mensaje y el horario almacenado
            mensaje = self.valor_mensajes.get()  # Asume que el mensaje está en un Entry
            horario = self.valor_horario.get()  # Asume que el horario está en un Entry

            # Verifica si el horario actual coincide con el horario registrado
            if horario == datetime.now().strftime("%H:%M"):
                # Muestra la notificación
                notification.notify(
                    title="¡Recordatorio!",
                    message=mensaje,
                    timeout=10  # Duración de la notificación
                )
           
            time.sleep(30)

    
    def iniciar_verificacion(self):
        
        verificador = threading.Thread(target=self.verificar_horario)
        verificador.daemon = True  # Permite que el hilo termine cuando la aplicación se cierre
        verificador.start()
    

    