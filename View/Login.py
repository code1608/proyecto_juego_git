import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from View.Tooltip import Tooltip
from View.CrearCuenta import CrearCuenta
from View.Ayuda import Ayuda
from tkinter import messagebox
from Controller.ControladorLogin import iniciar_sesion
from View.MenuPrincipal import MenuPrincipal
from View.InterfazJuego import InterfazJuego

class Login:

    
    def __init__(self):
        
        self.nombre_usuario = None
        
        self.IncioSesion = tk.Tk()
        self.IncioSesion.config(width=400, height=400)
        self.IncioSesion.resizable(0, 0)
        self.IncioSesion.title("Juego - Inicio Sesión")

        self.mostrarPassword = False

        self.iconoAyuda = PhotoImage(file=r"img\ayuda2.png")
        self.btnAyuda = tk.Button(self.IncioSesion, image=self.iconoAyuda, command=self.iconoAyuda)
        self.btnAyuda.place(x=340, y=20, width=40, height=40)

        self.IncioSesion.bind("<Alt-w>", self.ayuda)
        self.btnAyuda.bind("<Button-1>", self.ayuda)
        Tooltip(self.btnAyuda, "Ayuda (Alt-w)")

        self.lblLogin = Label(self.IncioSesion, text="Iniciar sesión", font=('Bauhaus 93', 25))
        self.lblLogin.place(x=120, y=30)
        self.txtLogin = Entry(self.IncioSesion, font=('Arial', 12), foreground="gray", highlightthickness=2)
        self.txtLogin.config(highlightbackground="red", highlightcolor="red")

        self.txtLogin.insert(0, "Ingrese su Usuario")
        self.txtLogin.bind("<FocusIn>", self.on_entry_click)
        self.txtLogin.bind("<FocusOut>", self.on_focus_out)
        self.txtLogin.place(x=150, y=145, height=25, width=140)

        self.iconoUser = tk.PhotoImage(file=r"img\usuario.png")
        self.btnUser = tk.Label(self.IncioSesion, image=self.iconoUser)
        self.btnUser.place(x=90, y=130, width=50, height=50)

        self.txtPassword = Entry(self.IncioSesion, font=('Arial', 12), foreground="gray", highlightthickness=2)
        self.txtPassword.config(highlightbackground="red", highlightcolor="red")
        self.txtPassword.insert(0, "Ingrese su Contraseña")
        self.txtPassword.bind("<FocusIn>", self.on_entry_click2)
        self.txtPassword.bind("<FocusOut>", self.on_focus_out2)
        self.txtPassword.place(x=150, y=215, height=25, width=160)

        self.iconoPassword = tk.PhotoImage(file=r"img\encerrar.png")
        self.btnPassword = tk.Label(self.IncioSesion, image=self.iconoPassword)
        self.btnPassword.place(x=90, y=200, width=50, height=50)
        
        self.iconoVer = PhotoImage(file=r"img\mostrar-contrasena.png")
        self.iconoOcultar = PhotoImage(file=r"img\ojo.png")

        self.btnVer = tk.Button(self.IncioSesion, image=self.iconoOcultar, command=self.verCaracteres)
        self.btnVer.place(x=320, y=200, width=40, height=40)
        self.tooltip_ver = Tooltip(self.btnVer, "Ocultar Contraseña")

        self.iconoIngresar = PhotoImage(file=r"img\entrar.png")
        self.btnIngresar = tk.Button(self.IncioSesion, image=self.iconoIngresar)
        self.btnIngresar.place(x=80, y=290, width=50, height=50)        
        self.IncioSesion.bind("<Alt-r>", self.validar_credenciales)
        self.btnIngresar.bind("<Button-1>", self.validar_credenciales)
        Tooltip(self.btnIngresar, "Ingresar al menú principal")


        self.iconoLimpiar = PhotoImage(file=r"img\limpiar.png")
        self.btnLimpiar = tk.Button(self.IncioSesion, image=self.iconoLimpiar)
        self.btnLimpiar.place(x=180, y=290, width=50, height=50)
        self.IncioSesion.bind("<Alt-l>", self.limpiar)
        self.btnLimpiar.bind("<Button-1>", self.limpiar)
        Tooltip(self.btnLimpiar, "Limpiar datos")

        self.iconoCrearCuenta = PhotoImage(file=r"img\crearCuenta.png")
        self.btnCrearCuenta = tk.Button(self.IncioSesion, image=self.iconoCrearCuenta, command=self.iconoCrearCuenta)
        self.btnCrearCuenta.place(x=280, y=290, width=50, height=50)
        self.btnCrearCuenta.bind("<Alt-x>", self.crearCuenta)
        self.btnCrearCuenta.bind("<Button-1>", self.crearCuenta)
        Tooltip(self.btnCrearCuenta, "Crear Cuenta")

        self.widgets = [self.txtLogin, self.txtPassword, self.btnIngresar, self.btnLimpiar, self.btnCrearCuenta, self.btnAyuda]
        self.current_index = 0

        self.IncioSesion.bind("<Tab>", self.handle_tab)
        self.IncioSesion.mainloop()
        
        
    
   
    def verCaracteres(self):
        """Alterna entre mostrar y ocultar los caracteres de la contraseña."""
        if self.mostrarPassword:
            self.txtPassword.config(show="")
            self.btnVer.config(image=self.iconoVer)
            self.tooltip_ver.update_text("Ocultar Contraseña")
        else:
            self.txtPassword.config(show="*")
            self.btnVer.config(image=self.iconoOcultar)
            self.tooltip_ver.update_text("Ver Contraseña")
        self.mostrarPassword = not self.mostrarPassword


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

    def limpiar(self, event):
        self.txtLogin.delete(0, END)
        self.txtPassword.delete(0, END)

    def ayuda(self, event):
        app = Ayuda()

    def crearCuenta(self, event):
        app = CrearCuenta()

    def on_entry_click(self, event):
        if self.txtLogin.get() == "Ingrese su Usuario":
            self.txtLogin.delete(0, tk.END)
            self.txtLogin.configure(foreground="black")

    def on_focus_out(self, event):
        if not self.txtLogin.get():
            self.txtLogin.insert(0, "Ingrese su Usuario")
            self.txtLogin.configure(foreground="gray")

    def on_entry_click2(self, event):
        if self.txtPassword.get() == "Ingrese su Contraseña":
            self.txtPassword.delete(0, tk.END)
            self.txtPassword.configure(foreground="black")

    def on_focus_out2(self, event):
        if not self.txtPassword.get():
            self.txtPassword.insert(0, "Ingrese su Contraseña")
            self.txtPassword.configure(foreground="gray")
    
    
    def validar_credenciales(self, event):
        """Valida las credenciales contra la base de datos."""
        nombre_usuario = self.txtLogin.get().strip()
        password = self.txtPassword.get().strip()

        if not nombre_usuario or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, completa ambos campos.")
            return

        try:
            # Validar en la base de datos y obtener el ID del usuario
            usuario_id = iniciar_sesion(nombre_usuario, password)  # Devuelve el ID del usuario o None
            print(f"ID del usuario autenticado: {usuario_id}")  # Depuración

            if usuario_id and isinstance(usuario_id, int):  # Verifica que el ID sea un número entero
                messagebox.showinfo("Inicio exitoso", f"¡Bienvenido, {nombre_usuario}!")

                # Abre el menú principal y pasa el ID del usuario
                app = MenuPrincipal(usuario_id)  # Pasa el ID al menú principal
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar con la base de datos: {e}")

