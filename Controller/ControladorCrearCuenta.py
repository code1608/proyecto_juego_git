import mysql.connector
from Model.ConexionDB import conectar_db  # Reutiliza conexión desde el modelo
from tkinter import messagebox

# Definición de constantes
TABLE_NAME = "Usuarios"
COLUMN_NAME = "nombre_usuario"
COLUMN_PASSWORD = "password"

def guardar_usuario(nombre, password):
    """
    Guarda un nuevo usuario en la base de datos, si el usuario no existe.
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Verificar si el usuario ya existe
        query_verificar = f"SELECT * FROM {TABLE_NAME} WHERE {COLUMN_NAME} = %s"
        cursor.execute(query_verificar, (nombre,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            messagebox.showwarning("Advertencia", "El nombre de usuario ya existe. Por favor, elige otro.")
            return False

        # Insertar el nuevo usuario
        query_insertar = f"INSERT INTO {TABLE_NAME} ({COLUMN_NAME}, {COLUMN_PASSWORD}) VALUES (%s, %s)"
        cursor.execute(query_insertar, (nombre, password))
        conexion.commit()
        return True

    except mysql.connector.Error as err:
        messagebox.showerror("Error de Base de Datos", f"Ocurrió un error: {err}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def validar_usuario(username, password):
    """
    Valida un usuario en la base de datos con nombre y contraseña.
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)
        
        # Consultar si el usuario y contraseña coinciden
        query = f"SELECT * FROM {TABLE_NAME} WHERE {COLUMN_NAME} = %s AND {COLUMN_PASSWORD} = %s"
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()
        return usuario

    except mysql.connector.Error as err:
        messagebox.showerror("Error de Base de Datos", f"Ocurrió un error: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
