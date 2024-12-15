import tkinter as tk
from tkinter import ttk
import datetime


class TablaPosicion:
    def __init__(self, puntajes):
        """
        Crea una ventana para mostrar la tabla de posiciones.
        :param puntajes: Lista de diccionarios con 'usuario', 'puntaje' y 'fecha'.
        """
        # Obtener el nombre del usuario, que podría ser el primero de los puntajes
        # Suponiendo que 'usuario' es una cadena que contiene el nombre
        nombre_usuario = puntajes[0]["usuario"] if puntajes else "Invitado"
        
        self.TablaPosicion = tk.Toplevel()
        self.TablaPosicion.title(f"Juego - {nombre_usuario}")  # Título con el nombre del usuario
        self.TablaPosicion.geometry("500x130")
        self.TablaPosicion.resizable(0, 0)

        # Etiqueta para la tabla con el nombre del usuario
        tk.Label(
            self.TablaPosicion, text=f"Tabla de Puntajes de {nombre_usuario}", font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Crear Treeview para mostrar los puntajes
        self.treeview = ttk.Treeview(
            self.TablaPosicion, columns=("Usuario", "Puntaje", "Fecha"), show="headings"
        )
        self.treeview.heading("Usuario", text="Usuario")
        self.treeview.heading("Puntaje", text="Puntaje")
        self.treeview.heading("Fecha", text="Fecha")
        self.treeview.column("Usuario", width=150, anchor="center")
        self.treeview.column("Puntaje", width=100, anchor="center")
        self.treeview.column("Fecha", width=200, anchor="center")
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)

        # Verificar que puntajes sea una lista válida antes de intentar llenarla
        if isinstance(puntajes, list) and puntajes:
            self.llenar_puntajes(puntajes)
        else:
            tk.Label(
                self.TablaPosicion,
                text="No hay puntajes disponibles para mostrar.",
                font=("Arial", 12),
                fg="red",
            ).pack(pady=10)

        # Botón para cerrar la ventana
        btn_cerrar = tk.Button(self.TablaPosicion, text="Cerrar", command=self.TablaPosicion.destroy)
        btn_cerrar.pack(pady=10)

        self.TablaPosicion.mainloop()

    def llenar_puntajes(self, puntajes):
        """
        Llena el Treeview con el puntaje más alto.
        :param puntajes: Lista de diccionarios con 'usuario', 'puntaje' y 'fecha'.
        """
        try:
            # Ordenar los puntajes de mayor a menor
            puntajes_ordenados = sorted(puntajes, key=lambda x: x['puntaje'], reverse=True)

            # Mostrar solo el puntaje más alto
            puntaje_maximo = puntajes_ordenados[0] if puntajes_ordenados else None

            if puntaje_maximo:
                # Verificar que el puntaje sea un número y que la fecha sea válida
                if isinstance(puntaje_maximo["puntaje"], (int, float)) and isinstance(puntaje_maximo["fecha"], (str, datetime.datetime)):
                    # Si 'fecha' es un objeto datetime, convertirlo a cadena
                    if isinstance(puntaje_maximo["fecha"], datetime.datetime):
                        puntaje_maximo["fecha"] = puntaje_maximo["fecha"].strftime('%Y-%m-%d %H:%M:%S')

                    # Insertar solo el puntaje máximo en el Treeview
                    self.treeview.insert(
                        "", "end", values=(puntaje_maximo["usuario"], puntaje_maximo["puntaje"], puntaje_maximo["fecha"])
                    )
            else:
                print("No hay puntajes disponibles.")
                
        except Exception as e:
            print(f"Error al llenar puntajes: {e}")
            # Mostrar error en la interfaz también
            tk.Label(self.TablaPosicion, text="Hubo un error al cargar los puntajes.", fg="red").pack(pady=10)
