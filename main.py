import sqlite3
DIC_SLANG = "dicslang.db"


def conectar():
    return sqlite3.connect(DIC_SLANG)


def tabla():
    tablas = [
        """
        CREATE TABLE IF NOT EXISTS diccionario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra TEXT NOT NULL,
            significado TEXT NOT NULL
        );
        """
    ]
    conexion = conectar()
    cursor = conexion.cursor()
    for tabla in tablas:
        cursor.execute(tabla)


def principal():
    tabla()
    menu = """
1) Agregar nueva palabra
2) Editar palabra existente
3) Eliminar palabra existente
4) Ver listado de palabras
5) Buscar significado de palabra
6) Salir
Elige: """
    eleccion = ""
    while eleccion != "6":
        eleccion = input(menu)
        if eleccion == "1":
            palabra = input("Ingresa la palabra: ")
            # Comprobar si no existe
            posible_significado = buscar_significado_palabra(palabra)
            if posible_significado:
                print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        if eleccion == "2":
            palabra = input("Ingresa la palabra que quieres editar: ")
            nuevo_significado = input("Ingresa el nuevo significado: ")
            editar_palabra(palabra, nuevo_significado)
            print("Palabra actualizada")
        if eleccion == "3":
            palabra = input("Ingresa la palabra a eliminar: ")
            eliminar_palabra(palabra)
        if eleccion == "4":
            palabras = obtener_palabras()
            print("=== Lista de palabras ===")
            for palabra in palabras:
                # Al leer desde la base de datos se devuelven los datos como arreglo, por
                # lo que hay que imprimir el primer elemento
                print(palabra[0])
        if eleccion == "5":
            palabra = input(
                "Ingresa la palabra de la cual quieres saber el significado: ")
            significado = buscar_significado_palabra(palabra)
            if significado:
                print(f"El significado de '{palabra}' es:\n{significado[0]}")
            else:
                print(f"Palabra '{palabra}' no encontrada")


def agregar_palabra(palabra, significado):
    conexion = conectar()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO diccionario(palabra, significado) VALUES (?, ?)"
    cursor.execute(sentencia, [palabra, significado])
    conexion.commit()


def editar_palabra(palabra, nuevo_significado):
    conexion = conectar()
    cursor = conexion.cursor()
    sentencia = "UPDATE diccionario SET significado = ? WHERE palabra = ?"
    cursor.execute(sentencia, [nuevo_significado, palabra])
    conexion.commit()


def eliminar_palabra(palabra):
    conexion = conectar()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM diccionario WHERE palabra = ?"
    cursor.execute(sentencia, [palabra])
    conexion.commit()


def obtener_palabras():
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = "SELECT palabra FROM diccionario"
    cursor.execute(consulta)
    return cursor.fetchall()


def buscar_significado_palabra(palabra):
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = "SELECT significado FROM diccionario WHERE palabra = ?"
    cursor.execute(consulta, [palabra])
    return cursor.fetchone()


if __name__ == '__main__':
    principal()
