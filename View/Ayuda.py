import tkinter as tk
from tkinter import *

class Ayuda:
    def __init__(self):
        self.Ayuda = tk.Toplevel()
        self.Ayuda.config(width=300, height=200)
        self.Ayuda.resizable(0,0)
        self.Ayuda.title("Ayuda - Información")
        
        
        self.lblAtajos = Label(self.Ayuda, text="Atajos de teclado", font=("Arial",15))
        self.lblAtajos.place(x=90, y=30)
        
        
        
        self.lblAtajoCrearCuenta = Label(self.Ayuda, text="Crear Cuenta     [ Alt-x ]", font=("Arial",12))
        self.lblAtajoCrearCuenta.place(x=70, y=80)
        
        
        self.lblAtajoLimpiar = Label(self.Ayuda, text="Limpiar               [ Alt-l ]", font=("Arial",12))
        self.lblAtajoLimpiar.place(x=80, y=110)
        
        
        
        self.lblAtajoMenuPrincipal = Label(self.Ayuda, text="Ingresar menú Principal   [ Alt-r ]", font=("Arial",12))
        self.lblAtajoMenuPrincipal.place(x=30, y=140)
        
        
        self.Ayuda.mainloop()
    