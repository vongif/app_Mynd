from tkinter import Tk, Frame
import vista


class Controlador:
    def __init__(self, aplicacion):
        self.aplicacion_controlador = aplicacion
        self.objeto_uno = vista.Ventana(self.aplicacion_controlador)


if __name__ == "__main__":
    aplicacion = Tk()
    aplicacion.title("Mynd")  #  título 
    aplicacion.iconbitmap("ico.ico")

    aplication = Controlador(aplicacion)

    aplication.objeto_uno.actualizar()
aplicacion.mainloop()