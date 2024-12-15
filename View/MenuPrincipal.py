import tkinter as tk
from tkinter import PhotoImage, messagebox
from View.Tooltip import Tooltip
from View.TablaPosicion import TablaPosicion
from View.InterfazJuego import InterfazJuego
from View.AyudaMenuPrincipal import AyudaMenuPrincipal
from Controller.ControladorTablaPosicion import obtener_puntajes

class MenuPrincipal:
    def __init__(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario  # Almacena el nombre de usuario en un atributo
        print(f"Usuario autenticado: {self.nombre_usuario}")  # Depuración: Verifica el valor de username

        self.MenuPrincipal = tk.Toplevel()
        self.MenuPrincipal.config(width=300, height=300)
        self.MenuPrincipal.resizable(0, 0)
        self.MenuPrincipal.title("Juego - Menú Principal")

        
        self.crear_botones()
        
        
        
        # Manejo de Tabulación
        self.widgets = [self.btnAyuda, self.btnPuntaje ,self.btnJugar, self.btnSalir]
        self.current_index = 0
        
        self.MenuPrincipal.bind("<Tab>", self.handle_tab)
        
        self.MenuPrincipal.mainloop()

    def crear_botones(self):
        """ Crea todos los botones del menú principal """
        self.crear_boton_puntajes()
        self.crear_boton_ayuda()
        self.crear_boton_jugar()
        self.crear_boton_salir()

    def crear_boton_puntajes(self):
        """ Crea el botón de tabla de puntuación """
        self.iconoPuntaje = PhotoImage(file=r"img\puntuacion.png")
        self.btnPuntaje = tk.Button(self.MenuPrincipal, image=self.iconoPuntaje)
        self.btnPuntaje.place(x=120, y=20, width=80, height=80)
        self.btnPuntaje.bind("<Alt-m>", self.tablaPosicion)
        self.btnPuntaje.bind("<Button-1>", self.tablaPosicion)
        self.MenuPrincipal.bind("<Alt-o>", self.tablaPosicion)
        self.btnPuntaje.bind("<Button-1>", self.tablaPosicion)
        Tooltip(self.btnPuntaje, "Tabla de puntuación")

    def crear_boton_ayuda(self):
        """ Crea el botón de ayuda """
        self.iconoAyuda = PhotoImage(file=r"img\ayuda2.png")
        self.btnAyuda = tk.Button(self.MenuPrincipal, image=self.iconoAyuda)
        self.btnAyuda.place(x=240, y=20, width=40, height=40)
        self.MenuPrincipal.bind("<Alt-w>", self.ayuda3)
        self.btnAyuda.bind("<Button-1>", self.ayuda3)
        Tooltip(self.btnAyuda, "Ayuda (Alt-w)")

    def crear_boton_jugar(self):
        """ Crea el botón de jugar """
        self.iconoJugar = PhotoImage(file=r"img\jugar2.png")
        self.btnJugar = tk.Button(self.MenuPrincipal, image=self.iconoJugar, command=self.iniciar_juego)
        self.btnJugar.place(x=120, y=112, width=80, height=80)
        self.MenuPrincipal.bind("<Alt-m>", self.iniciar_juego)
        self.btnJugar.bind("<Button-1>", self.iniciar_juego)
        Tooltip(self.btnJugar, "Jugar")

    def crear_boton_salir(self):
        """ Crea el botón de salir """
        self.iconoSalir = PhotoImage(file=r"img\cerrar-sesion.png")
        self.btnSalir = tk.Button(self.MenuPrincipal, image=self.iconoSalir, command=self.salir)
        self.btnSalir.place(x=120, y=205, width=80, height=80)
        self.MenuPrincipal.bind("<Alt-z>", self.salir)
        self.btnSalir.bind("<Button-1>", self.salir)
        Tooltip(self.btnSalir, "Salir")
        

    
    def handle_tab(self, event):
        # Remove focus highlight from the current widget
        current_widget = self.widgets[self.current_index]
        if isinstance(current_widget, tk.Entry):
            current_widget.config(highlightbackground="gray", highlightcolor="gray")
        elif isinstance(current_widget, tk.Button):
            current_widget.config(relief=tk.RAISED)

        # Move to the next widget
        self.current_index = (self.current_index + 1) % len(self.widgets)
        next_widget = self.widgets[self.current_index]
        next_widget.focus_set()

        # Highlight the next widget
        if isinstance(next_widget, tk.Entry):
            next_widget.config(highlightbackground="blue", highlightcolor="blue")
        elif isinstance(next_widget, tk.Button):
            next_widget.config(relief=tk.SUNKEN)
        return "break"



    def ayuda3(self, event=None):
        app = AyudaMenuPrincipal()


    def tablaPosicion(self, event=None):
        try:
            # Convertir self.username a ID si es necesario
            user_id = int(self.nombre_usuario)  # Asegúrate de que sea un entero
            print(f"Obteniendo puntajes para el usuario: {self.nombre_usuario}")  # Depuración
            
            # Obtener los puntajes desde la base de datos
            puntajes = obtener_puntajes(user_id)
            
            # Depuración: Verificar el tipo y contenido de puntajes
            print(f"Tipo de puntajes: {type(puntajes)}")  # Verifica que sea una lista
            print(f"Puntajes obtenidos: {puntajes}")  # Muestra los puntajes obtenidos
            
            if puntajes:  # Si hay puntajes, los mostramos
                TablaPosicion(puntajes)
            else:
                messagebox.showinfo("Sin puntajes", "No se encontraron puntajes para este usuario.")
        except ValueError:
            messagebox.showerror("Error", "El ID del usuario debe ser un número válido.")
        except Exception as e:
            print(f"Error al obtener la tabla de posiciones: {e}")
            messagebox.showerror("Error", f"Error al obtener los puntajes: {e}")

    def iniciar_juego(self, event=None):
        try:
            print(f"Iniciando juego para el usuario con ID: {self.nombre_usuario}")  # Cambia a usuario_actual
            juego = InterfazJuego(self.nombre_usuario)  # Usa el ID almacenado
            juego.ejecutar()
        except Exception as e:
            messagebox.showerror("Error al iniciar el juego", f"{e}")

    def salir(self, event=None):
        """ Cierra el menú y vuelve al inicio de sesión o donde sea necesario """
        respuesta = messagebox.askyesno("Confirmar salida", "¿Estás seguro de que quieres salir?")
        if respuesta:  # Solo destruir la ventana si el usuario confirma
            self.MenuPrincipal.destroy()
