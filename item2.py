import hashlib
import sqlite3
from getpass import getpass

def crear_tabla_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_apellido TEXT NOT NULL,
            registro_elegido TEXT NOT NULL,
            hash_contraseña TEXT NOT NULL
        )
    ''')
    conn.commit()

def insertar_usuario(conn, nombre_apellido, registro_elegido, hash_contraseña):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nombre_apellido, registro_elegido, hash_contraseña)
        VALUES (?, ?, ?)
    ''', (nombre_apellido, registro_elegido, hash_contraseña))
    conn.commit()

def obtener_hash_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode('utf-8')).hexdigest()

def validar_usuario(conn, nombre_apellido, registro_elegido, contraseña):
    hash_contraseña = obtener_hash_contraseña(contraseña)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios
        WHERE nombre_apellido = ? AND registro_elegido = ? AND hash_contraseña = ?
    ''', (nombre_apellido, registro_elegido, hash_contraseña))
    usuario = cursor.fetchone()
    return usuario is not None

def main():
    conn = sqlite3.connect('usuarios.db')
    crear_tabla_usuarios(conn)

    nombre_apellido = input("Ingrese su nombre y apellido: ")
    registro_elegido = input("Ingrese otro registro elegido: ")
    contraseña = getpass("Ingrese su contraseña: ")

    hash_contraseña = obtener_hash_contraseña(contraseña)

    insertar_usuario(conn, nombre_apellido, registro_elegido, hash_contraseña)
    print("Usuario registrado correctamente.")

    if validar_usuario(conn, nombre_apellido, registro_elegido, contraseña):
        print("Usuario validado correctamente.")
    else:
        print("Error al validar el usuario.")

    conn.close()

if __name__ == "__main__":
    main()
