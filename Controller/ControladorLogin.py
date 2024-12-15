import mysql.connector
from Model.ConexionDB import conectar_db
from tkinter import messagebox

# Variable global para el usuario autenticado
usuario_actual = None

def iniciar_sesion(nombre, password):
    """
    Autentica al usuario y devuelve su ID si las credenciales son válidas.
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "SELECT id_usuario, password FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(query, (nombre,))
        resultado = cursor.fetchone()

        if resultado and resultado[1] == password:  # Comparar contraseñas
            return resultado[0]  # Devuelve el ID del usuario (número entero)
        else:
            return None
    except Exception as e:
        raise e
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
