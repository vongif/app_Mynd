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
from threading import Thread
import tkinter as tk


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
    


    def mostrar_notificacion(self, mensaje, duracion=5):
        ventana = tk.Toplevel()
        ventana.geometry("500x250")  # Tamaño de la ventana
        ventana.configure(bg="red")  # Fondo rojo
        ventana.overrideredirect(True)  # Quitar barra de título
        ventana.attributes("-topmost", True)  # Siempre visible

        # Centrar la ventana en la pantalla
        ventana.update_idletasks()
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (300 // 2)
        y = (alto_pantalla // 2) - (100 // 2)
        ventana.geometry(f"+{x}+{y}")

        # Texto de la notificación
        etiqueta = tk.Label(
           ventana,
            text=mensaje,
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg="red",
            wraplength=350,  # Ajusta el texto si es muy largo
            justify="center",
        )
        etiqueta.pack(pady=20)
        # Botón para cerrar la ventana
        boton_aceptar = tk.Button(
            ventana,
            text="Aceptar",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="red",
            command=ventana.destroy,  # Cierra la ventana
        )
        boton_aceptar.pack(pady=10)
       
        ventana.mainloop()




    def verificar_horario(self):
        while True:
            registros = Mensajes.select()  # Recupera todos los mensajes y horarios
            for registro in registros:
                if registro.horario == datetime.now().strftime("%H:%M"):
                    Thread(target=self.mostrar_notificacion, args=(registro.mensajes,)).start()
                
            time.sleep(30)

    
    def iniciar_verificacion(self):
        
        verificador = threading.Thread(target=self.verificar_horario)
        verificador.daemon = True  # Permite que el hilo termine cuando la aplicación se cierre
        verificador.start()
    



    #---------Prueba-------------------------------------------------------------------------------------
    
    def funcion_buscar(
        self,
        tree,
        busqueda,
    ):

        busqueda = busqueda.get()
        records = tree.get_children()
        global my_data
        for element in records:
            tree.delete(element)
            buscar = (
                Clientes.select().where(Clientes.id.contains(busqueda))
                | Clientes.select().where(Clientes.cuenta.contains(busqueda))
                | Clientes.select().where(Clientes.reparto.contains(busqueda))
                | Clientes.select().where(Clientes.numero_de_cliente.contains(busqueda))
                | Clientes.select().where(Clientes.sucursal.contains(busqueda))
                | Clientes.select().where(Clientes.razonsocial.contains(busqueda))
                | Clientes.select().where(Clientes.direccion.contains(busqueda))
                | Clientes.select().where(Clientes.localidad.contains(busqueda))
            )
            buscar.execute()
        try:
            for fila in buscar:
                tree.insert(
                    "",
                    "end",
                    text=fila.id,
                    values=(
                        fila.cuenta,
                        fila.reparto,
                        fila.numero_de_cliente,
                        fila.sucursal,
                        fila.razonsocial,
                        fila.direccion,
                        fila.localidad,
                    ),
                )
        except:
            print(f"No se enontro ningun registro con la busqueda: '{busqueda}'")
        else:
            print(
                f"El resultado es :  ID={fila.id}, Cuenta={fila.cuenta}, Reparto={fila.reparto}, Razon Social={fila.razonsocial}"
            )
