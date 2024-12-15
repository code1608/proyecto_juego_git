import tkinter as tk
from tkinter import *

class AyudaCrearCuenta:
    def __init__(self):
        self.AyudaCrearCuenta = tk.Toplevel()
        self.AyudaCrearCuenta.config(width=300, height=200)
        self.AyudaCrearCuenta.resizable(0,0)
        self.AyudaCrearCuenta.title("Ayuda - Información")
        
        
        self.lblAtajos = Label(self.AyudaCrearCuenta, text="Atajos de teclado", font=("Arial",15))
        self.lblAtajos.place(x=90, y=30)
        
        
        
        self.lblAtajoCrear = Label(self.AyudaCrearCuenta, text="Crear  [ Alt-p ]", font=("Arial",12))
        self.lblAtajoCrear.place(x=70, y=80)
        
        
        self.lblAtajoLimpiar = Label(self.AyudaCrearCuenta, text="Limpiar [ Alt-l ]", font=("Arial",12))
        self.lblAtajoLimpiar.place(x=70, y=110)
        
        
    
        
        
        self.AyudaCrearCuenta.mainloop()
    