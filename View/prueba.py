import tkinter as tk

# Función para manejar el evento del tabulador
def on_tab_press(event):
    widget = event.widget  # Obtiene el widget actual
    widget.focus_set()     # Establece el foco en el widget
    highlight_widget(widget)  # Llama a la función para resaltar

# Función para resaltar el widget con enfoque
def highlight_widget(widget):
    # Cambia el borde del widget activo
    widget.config(highlightbackground="blue", highlightthickness=2)
    
    # Limpia los bordes de otros widgets
    for w in widgets:
        if w != widget:
            w.config(highlightbackground="gray", highlightthickness=1)

# Crear la ventana principal
root = tk.Tk()
root.title("Tabulación en Tkinter")

# Lista de widgets para resaltar
widgets = []

# Crear widgets
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
button = tk.Button(root, text="Presiona Tab")

# Añadir widgets a la lista
widgets.extend([entry1, entry2, button])

# Colocar widgets en la ventana
entry1.grid(row=0, column=0, padx=10, pady=10)
entry2.grid(row=1, column=0, padx=10, pady=10)
button.grid(row=2, column=0, padx=10, pady=10)

# Asignar evento de tecla Tab a los widgets
for widget in widgets:
    widget.bind("<Tab>", on_tab_press)

# Iniciar el bucle principal
root.mainloop()
