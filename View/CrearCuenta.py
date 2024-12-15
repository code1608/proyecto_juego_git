import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from View.Tooltip import Tooltip
from View.AyudaCrearCuenta import AyudaCrearCuenta
from Controller.ControladorCrearCuenta import guardar_usuario
from tkinter import messagebox


class CrearCuenta:
    def __init__(self):
        self.CrearCuenta = tk.Toplevel()
        self.CrearCuenta.config(width=400, height=400)
        self.CrearCuenta.resizable(0, 0)
        self.CrearCuenta.title("Juego - Crear Cuenta")

        # Botón de Ayuda
        self.iconoAyuda2 = PhotoImage(file=r"img\ayuda2.png")
        self.btnAyuda2 = tk.Button(self.CrearCuenta, image=self.iconoAyuda2, command=self.ayuda2)
        self.btnAyuda2.place(x=340, y=20, width=40, height=40)
        self.CrearCuenta.bind("<Alt-w>", self.ayuda2)
        self.btnAyuda2.bind("<Button-1>", self.ayuda2)
        Tooltip(self.btnAyuda2, "Ayuda (Alt-w)")

        
        # Etiqueta principal
        self.lblLogin = Label(self.CrearCuenta, text="Crear Cuenta", font=('Bauhaus 93', 25))
        self.lblLogin.place(x=120, y=30)
        self.txtLogin = Entry(self.CrearCuenta, font=('Arial', 12), foreground="gray", highlightthickness=2)
        self.txtLogin.config(highlightbackground="red", highlightcolor="red")
        self.txtLogin.insert(0, "Usuario Nuevo")
        self.txtLogin.bind("<FocusIn>", self.on_entry_click)
        self.txtLogin.bind("<FocusOut>", self.on_focus_out)
        self.txtLogin.place(x=150, y=145, height=25, width=140)

        self.iconoUser = PhotoImage(file=r"img\usuario.png")
        self.btnUser = tk.Label(self.CrearCuenta, image=self.iconoUser)
        self.btnUser.place(x=90, y=130, width=50, height=50)
        self.txtPassword = Entry(self.CrearCuenta, font=('Arial', 12), foreground="gray", highlightthickness=2)
        self.txtPassword.config(highlightbackground="red", highlightcolor="red")
        self.txtPassword.insert(0, "Contraseña Nueva")
        self.txtPassword.bind("<FocusIn>", self.on_entry_click2)
        self.txtPassword.bind("<FocusOut>", self.on_focus_out2)
        self.txtPassword.place(x=150, y=215, height=25, width=160)

        self.iconoPassword = PhotoImage(file=r"img\encerrar.png")
        self.btnPassword = tk.Label(self.CrearCuenta, image=self.iconoPassword)
        self.btnPassword.place(x=90, y=200, width=50, height=50)

        # Botón de Crear
        self.iconoCrear = PhotoImage(file=r"img\boligrafo.png")
        self.btnCrear = tk.Button(self.CrearCuenta, image=self.iconoCrear, command=self.crear_user)
        self.btnCrear.place(x=130, y=290, width=50, height=50)
        self.CrearCuenta.bind("<Alt-p>", self.crear_user)
        self.btnCrear.bind("<Button-1>", self.crear_user)
        Tooltip(self.btnCrear, "Crear")

        # Botón de Limpiar
        self.iconoLimpiar = PhotoImage(file=r"img\limpiar.png")
        self.btnLimpiar = tk.Button(self.CrearCuenta, image=self.iconoLimpiar)
        self.btnLimpiar.place(x=240, y=290, width=50, height=50)
        self.CrearCuenta.bind("<Alt-l>", self.limpiar_campos)
        self.btnLimpiar.bind("<Button-1>", self.limpiar_campos)
        Tooltip(self.btnLimpiar, "Limpiar datos")

        # Manejo de Tabulación
        self.widgets = [self.txtLogin, self.txtPassword, self.btnCrear, self.btnLimpiar, self.btnAyuda2]
        self.current_index = 0

        self.CrearCuenta.bind("<Tab>", self.handle_tab)

        self.CrearCuenta.mainloop()

    
    
    def handle_tab(self, event):
        # Remove focus highlight from the current widget
        current_widget = self.widgets[self.current_index]
        if isinstance(current_widget, Entry):
            current_widget.config(highlightbackground="gray", highlightcolor="gray")
        elif isinstance(current_widget, Button):
            current_widget.config(relief=tk.RAISED)

        # Move to the next widget
        self.current_index = (self.current_index + 1) % len(self.widgets)
        next_widget = self.widgets[self.current_index]
        next_widget.focus_set()

        # Highlight the next widget
        if isinstance(next_widget, Entry):
            next_widget.config(highlightbackground="blue", highlightcolor="blue")
        elif isinstance(next_widget, Button):
            next_widget.config(relief=tk.SUNKEN)
        return "break"


    def crear_user(self, event):
        """
        Maneja la creación de usuarios.
        """
        nombre = self.txtLogin.get().strip()
        password = self.txtPassword.get().strip()
        
        if not nombre or nombre == "Usuario Nuevo" or not password or password == "Contraseña Nueva":
            messagebox.showwarning("Advertencia", "Completar todos los campos.")
            return

        if guardar_usuario(nombre, password):
            messagebox.showinfo("Información", f"Cuenta creada exitosamente para {nombre}.")
            self.limpiar_campos(event)
        else:
            messagebox.showerror("Error", "No se pudo crear la cuenta. Intenta con otro nombre.")
            

    def limpiar_campos(self, event):
        """
        Limpia los campos del formulario.
        """
        self.txtLogin.delete(0, END)
        self.txtPassword.delete(0, END)
        
    


    def ayuda2(self, event=None):
        """
        Muestra la ventana de ayuda.
        """
        app = AyudaCrearCuenta()

    def on_entry_click(self, event):
        """
        Limpia el texto de entrada predeterminado al hacer clic.
        """
        if self.txtLogin.get() == "Usuario Nuevo":
            self.txtLogin.delete(0, tk.END)
            self.txtLogin.configure(foreground="black")

    def on_focus_out(self, event):
        """
        Restaura el texto predeterminado si el campo está vacío.
        """
        if not self.txtLogin.get():
            self.txtLogin.insert(0, "Usuario Nuevo")
            self.txtLogin.configure(foreground="gray")

    def on_entry_click2(self, event):
        """
        Limpia el texto de entrada predeterminado de la contraseña al hacer clic.
        """
        if self.txtPassword.get() == "Contraseña Nueva":
            self.txtPassword.delete(0, tk.END)
            self.txtPassword.configure(foreground="black")
            self.txtPassword.config(show="*")

    def on_focus_out2(self, event):
        """
        Restaura el texto predeterminado de la contraseña si el campo está vacío.
        """
        if not self.txtPassword.get():
            self.txtPassword.insert(0, "Contraseña Nueva")
            self.txtPassword.configure(foreground="gray")
            self.txtPassword.config(show="")
