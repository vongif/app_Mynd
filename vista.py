from tkinter import IntVar
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from tkinter import Tk
from tkinter import Frame
from modelo import operaciones
from datetime import datetime



class Ventana:
    def __init__(self, ventana):
        self.objeto_uno = operaciones()
        self.aplicacion = ventana

        self.valor_mensajes = StringVar()
        self.valor_busqueda = StringVar()
        self.valor_horario = StringVar()

        self.titulo = Label(
            self.aplicacion,
            text="Gestion de Avisos",
            bg="DodgerBlue3",
            fg="White",
            height=2,
            width=55,
            font=("Arial", 16, "bold"),
        )
        self.titulo.grid(
            row=0, column=0, columnspan=4, sticky="we", padx=5, pady=5
        )

        

        # Entrada de mensaje
        Label(self.aplicacion, text="Mensaje:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_mensajes = ttk.Entry(self.aplicacion, textvariable=self.valor_mensajes, width=50)
        self.entry_mensajes.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Entrada de horario
        ttk.Label(self.aplicacion, text="Horario (HH:MM):", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_horario = ttk.Entry(self.aplicacion, textvariable=self.valor_horario, width=50)
        self.entry_horario.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Entrada de búsqueda
        Label(self.aplicacion, text="Buscar:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_busqueda = ttk.Entry(self.aplicacion, textvariable=self.valor_busqueda, width=50)
        self.entry_busqueda.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Frame para los botones
        self.botones_frame = Frame(self.aplicacion)
        self.botones_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")

        # Botones dentro del Frame
        self.boton_alta = Button(self.botones_frame, text="Alta", bg="royal blue", fg="white", command=lambda: self.aviso_alta(self.valor_mensajes, self.tree))
        self.boton_alta.grid(row=0, column=0, padx=5, pady=5)

        self.boton_modificar = Button(self.botones_frame, text="Modificar", bg="royal blue", fg="white", command=lambda: self.aviso_modificar())
        self.boton_modificar.grid(row=0, column=1, padx=5, pady=5)

        self.boton_borrar = Button(self.botones_frame, text="Eliminar", bg="royal blue", fg="white", command=lambda: self.aviso_borrar(self.tree))
        self.boton_borrar.grid(row=0, column=2, padx=5, pady=5)

        self.boton_actualizar = Button(self.botones_frame, text="Actualizar", bg="royal blue", fg="white", command=self.actualizar)
        self.boton_actualizar.grid(row=0, column=3, padx=5, pady=5)

        # Configurar las filas y columnas
        self.aplicacion.grid_rowconfigure(0, weight=1)
        self.aplicacion.grid_rowconfigure(1, weight=0)
        self.aplicacion.grid_rowconfigure(2, weight=0)
        self.aplicacion.grid_rowconfigure(3, weight=0)
        self.aplicacion.grid_rowconfigure(4, weight=1)
        self.aplicacion.grid_rowconfigure(5, weight=0)  # Fila para el botón de salir

        self.aplicacion.grid_columnconfigure(0, weight=1)
        self.aplicacion.grid_columnconfigure(1, weight=3)
        self.aplicacion.grid_columnconfigure(2, weight=1)
        self.aplicacion.grid_columnconfigure(3, weight=1)

        # TREEVIEW
        self.tree = ttk.Treeview(self.aplicacion, columns=("col1", "col2"), show="headings")
        self.tree.heading("col1", text="Mensaje")
        self.tree.column("col1", width=300, anchor="w")
        self.tree.heading("col2", text="Horario")
        self.tree.column("col2", width=100, anchor="center")
        self.tree.grid(row=5, column=0, columnspan=4, padx=5, pady=10, sticky="nsew")

        # Scrollbar
        self.scroll = ttk.Scrollbar(self.aplicacion, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=5, column=4, sticky="ns")
        self.tree.config(yscrollcommand=self.scroll.set)

        # Botón de salir
        self.boton_salir = Button(self.aplicacion, text="Salir", bg="RoyalBlue", fg="white", command=self.aplicacion.quit)
        self.boton_salir.grid(row=6, column=3, padx=30, pady=10, sticky="e")

        # Asocia el evento <<TreeviewSelect>> al TreeView
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)





    # METODOS-----------------------------------------------------------

    """def aviso_alta(self, valor_mensajes, tree):
        retorno = self.objeto_uno.funcion_alta(
            self.valor_mensajes,
            tree,
        )
        if messagebox.showinfo("Base Clientes", retorno):
            Label(
                self.aplicacion, font="Courier, 10", fg="blue2"
            ).place(x=280, y=100)
        else:
            messagebox.showinfo("Base Clientes", retorno)
"""

    def aviso_alta(self, valor_mensajes, tree):
        mensaje = self.valor_mensajes.get().strip()
        horario = self.valor_horario.get().strip()

        # Verificar que ambos campos estén completos
        if not mensaje or not horario:
            messagebox.showwarning("Advertencia", "Debes ingresar tanto un mensaje como un horario.")
            return

        # Opcional: Validar formato del horario
        try:
         datetime.strptime(horario, "%H:%M")  # Valida si el formato del horario es correcto
        except ValueError:
            messagebox.showerror("Error", "El horario debe estar en formato HH:MM.")
            return

        # Llama a la función de alta
        retorno = self.objeto_uno.funcion_alta(
        self.valor_mensajes,
        tree,
        )
        if messagebox.showinfo("Base Clientes", retorno):
         Label(
            self.aplicacion, font="Courier, 10", fg="blue2"
            ).place(x=280, y=100)
        else:
            messagebox.showinfo("Base Clientes", retorno)
    


    def aviso_borrar(self, tree):
        retorno = self.objeto_uno.funcion_borrar(tree)
        messagebox.showinfo("Base Clientes", retorno)
        
  

    
    def seleccionar_registro(self, event):
        # Obtiene el registro seleccionado
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado[0])  # Obtiene datos del registro
            mensaje = item["values"][0]  # Extrae el valor del mensaje
            self.valor_mensajes.set(mensaje) 
             # Muestra el mensaje en el Entry
    
               

    def aviso_modificar(self):
        retorno = self.objeto_uno.funcion_modificar(
            self.valor_mensajes,
            self.tree,
        )
        messagebox.showinfo("Base Clientes", retorno)
      

        
    def actualizar(
        self,
    ):
        self.objeto_uno.funcion_actualizar(self.tree)

