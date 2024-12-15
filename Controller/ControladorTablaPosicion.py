import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Model.ConexionDB import conectar_db
import mysql.connector


def registrar_puntaje(usuario, puntaje):
    """
    Registra el puntaje de un usuario en la base de datos.
    :param usuario: ID del usuario autenticado.
    :param puntaje: Puntaje obtenido en el juego.
    """
    if not usuario:
        messagebox.showerror("Error", "No hay usuario autenticado.")
        return
    
    print(f"usuario: {usuario}, tipo: {type(usuario)}")

    if not isinstance(usuario, int):
        messagebox.showerror("Error", "El ID del usuario debe ser un número entero.")
        return

    if puntaje < 2000:
        messagebox.showinfo("Puntaje no registrado", "El puntaje debe ser mayor o igual a 2000 para registrarse.")
        return

    if not isinstance(puntaje, int):
        messagebox.showerror("Error", "El puntaje debe ser un número entero.")
        return

    try:
        
        usuario = int(usuario)
        
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Insertar el puntaje en la tabla de puntajes (sin incluir la columna 'fecha')
        query = "INSERT INTO puntajes (id_usuario, puntaje) VALUES (%s, %s)"
        cursor.execute(query, (usuario, puntaje))
        conexion.commit()

        messagebox.showinfo("Éxito", "Puntaje registrado con éxito")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el puntaje: {str(e)}")
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
def obtener_puntajes(usuario_id):
    """
    Obtiene los puntajes de un usuario de la base de datos.
    :param usuario_id: ID del usuario.
    :return: Lista de puntajes del usuario o lista vacía en caso de error.
    """
    puntajes = []  # Inicializa la lista de puntajes vacía
    try:
        conexion = conectar_db()  # Establece la conexión a la base de datos
        cursor = conexion.cursor()

        # Consulta para obtener los puntajes del usuario con id_usuario en lugar de usuario
        query = "SELECT id_usuario, puntaje, fecha FROM puntajes WHERE id_usuario = %s ORDER BY puntaje DESC"
        cursor.execute(query, (usuario_id,))

        # Recupera todos los resultados como lista
        puntajes = cursor.fetchall()

        # Asegúrate de devolver una lista con solo los puntajes
        if puntajes:  # Si hay resultados
            return [{"usuario": p[0], "puntaje": p[1], "fecha": p[2]} for p in puntajes]
        else:
            return []  # Retorna una lista vacía si no hay puntajes

    except Exception as e:
        print(f"Error al obtener los puntajes: {e}")
        return []  # Devuelve una lista vacía en caso de error

    finally:
        # Cierra la conexión solo si fue creada
        if 'conexion' in locals() and conexion:
            conexion.close()
