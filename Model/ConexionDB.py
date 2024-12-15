import mysql.connector

def conectar_db():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="juego_spac"
    )
    return conexion
