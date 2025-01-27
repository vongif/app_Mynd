

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
import pywhatkit
import pywhatkit as kit

db = SqliteDatabase("base_ejemplo.db")


class BaseModel(Model):
    class Meta:
        database = db


class Mensajes(BaseModel):
    
        mensajes = CharField()
        horario = CharField()
        telefono = CharField()


db.connect()
db.create_tables([Mensajes])


class operaciones:
    def __init__(self, valor_mensajes, valor_horario, valor_telefono):

        self.valor_mensajes = valor_mensajes  # Inicializa las variables
        self.valor_horario = valor_horario
        self.valor_telefono = valor_telefono
        
        self.iniciar_verificacion()
        

    # Funciones CRUD-------------------------------------------------------------------------
   


    def funcion_alta(self, mensajes, horario, telefono, tree):
        texto = mensajes.get().strip()  # Ahora obtendrás el texto del StringVar
        hora = horario.get().strip()
        phone = telefono.get().strip()
        
        if not texto or not hora:
            return "Error: El mensaje o el Horario estan vacios."

        # Verifica la expresión regular
        expresion = "^[a-zA-ZÀ-ÿ0-9\s]+$"
        if re.match(expresion, texto):
            
                try:
                    datetime.strptime(hora, "%H:%M") 
                except ValueError:
                    return "Error: El horario debe estar en formato HH:MM."
                

                if not phone.isdigit() or len(phone) != 8:  # Asegurarse de que tenga solo 8 dígitos
                    return "Error: El número de teléfono debe contener 8 dígitos y no incluir prefijos."

                # Agregar automáticamente los prefijos
                codigo_pais = "54"  # Código de país
                codigo_area = "11"  # Código de área (ajústalo según sea necesario)
                telefono_completo = f"{codigo_pais}{codigo_area}{phone}"
                nuevo_mensaje = Mensajes(mensajes=texto, horario=hora, telefono=telefono_completo)

                #nuevo_mensaje = Mensajes(mensajes=texto, horario=hora, telefono=phone)
                nuevo_mensaje.save()

                self.funcion_actualizar(tree)
                mensajes.set("")  # Limpia el campo después de guardar
                horario.set("")
                telefono.set("")

                current_time = datetime.now().strftime("%H:%M")
                if current_time == hora:
                    # Enviar mensaje de WhatsApp si la hora coincide
                    self.funcion_enviar(telefono_completo, texto)
        


                return "Registro dado de alta"
        else:
                return "Error: El mensaje no cumple con el formato."




    def funcion_enviar(self, telefono, mensaje):
        try:
            kit.sendwhatmsg_instantly(
                phone_no=f"+{telefono}",
                message=mensaje,
                wait_time=20,  # Tiempo de espera en segundos antes de enviar
                tab_close=True  # Cierra la pestaña tras enviar
            )
            # Agregar un pequeño retraso para asegurarse de que el mensaje se haya enviado correctamente
            time.sleep(5)  # Espera 5 segundos para asegurarse de que el mensaje se envíe

            # Ahora cerrar la pestaña
            kit.close_tab()  # Si kit tiene una función close_tab(), úsala para cerrar la pestaña

            return "Mensaje enviado correctamente."
        except Exception as e:
            return f"Error al enviar el mensaje: {str(e)}"    




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
                    fila.telefono,
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
        telefono,
        tree,
    ):
        cliente = tree.selection()
        item = tree.item(cliente)
        mi_id = item["text"]
        actualizar = Mensajes.update(mensajes=mensajes.get(), horario=horario.get(), telefono=telefono.get()).where(Mensajes.id == mi_id)
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
    



        
    def funcion_buscar(
        self,
        tree,
        mensajes,
        horario_busqueda,
        telefono_busqueda,
        ):

        mensajes_busqueda = mensajes.get().strip()
        horario = horario_busqueda.get().strip()
        telefono = telefono_busqueda.get().strip()
        records = tree.get_children()
        
        for element in records:
            tree.delete(element)
            
            
        try:
            consulta = Mensajes.select()
            if mensajes_busqueda:
                consulta = consulta.where(Mensajes.mensajes.contains(mensajes_busqueda))

            if horario:
                consulta = consulta.where(Mensajes.horario.contains(horario))

            if telefono:
                consulta = consulta.where(Mensajes.telefono.contains(telefono))            

                
            for fila in consulta:
                tree.insert(
                    "",
                    "end",
                    text=fila.id,
                    values=(fila.mensajes, fila.horario, fila.telefono),
                )
                      
        except Exception as e:
            print(f"Error al ejecutar la busqueda: {e}")





    def enviar_mensaje_whatsapp(self, mensaje, numero):
        try:
            hora_actual = datetime.now()
            hora_envio = hora_actual.hour
            minuto_envio = hora_actual.minute + 1  # Envía el mensaje un minuto después de la ejecución
            
            # Envía el mensaje
            pywhatkit.sendwhatmsg(
                phone_no=f"+{numero}",  # Asegúrate de usar el formato internacional del número
                message=mensaje,
                time_hour=hora_envio,
                time_min=minuto_envio,
            )
            print(f"Mensaje enviado a {numero}: {mensaje}")
        except Exception as e:
            print(f"Error al enviar el mensaje de WhatsApp: {e}")




    def verificar_horario(self):
        while True:
            registros = Mensajes.select()  # Recupera todos los mensajes y horarios
            for registro in registros:
                if registro.horario == datetime.now().strftime("%H:%M"):
                    # Llama al método para enviar el mensaje por WhatsApp
                    self.enviar_mensaje_whatsapp(registro.mensajes, registro.telefono)
                    
                    # También muestra la notificación en la aplicación
                    Thread(target=self.mostrar_notificacion, args=(registro.mensajes,)).start()
                
            time.sleep(30) 
            


