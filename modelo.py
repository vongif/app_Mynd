import sqlite3
import re
from peewee import *


db = SqliteDatabase("base_ejemplo.db")


class BaseModel(Model):
    class Meta:
        database = db


class Mensajes(BaseModel):
    
        mensajes = CharField()


db.connect()
db.create_tables([Mensajes])


class operaciones:
    def __init__(self):
        pass

    # Funciones CRUD-------------------------------------------------------------------------

    def funcion_alta(self, mensajes, tree):
        texto = mensajes.get().strip()  # Ahora obtendrás el texto del StringVar
        if not texto:
            return "Error: El mensaje está vacío."

        # Verifica la expresión regular
        expresion = "^[a-zA-ZÀ-ÿ0-9\s]+$"
        if re.match(expresion, texto):
            nuevo_mensaje = Mensajes(mensajes=texto)
            nuevo_mensaje.save()

            self.funcion_actualizar(tree)
            mensajes.set("")  # Limpia el campo después de guardar
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
        tree,
    ):
        cliente = tree.selection()
        item = tree.item(cliente)
        mi_id = item["text"]
        actualizar = Mensajes.update(mensajes=mensajes.get()).where(Mensajes.id == mi_id)
        actualizar.execute() 
        
        self.funcion_actualizar(tree)
        mensajes.set("")
        return "Registro modificado"
    