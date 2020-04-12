"""Archivo contiene todas las funciones del programa
Le he agregado true y false para la posterior realizacion de
los test"""

import pymysql
def crea_lista_simple(conexion):
    """Elimina la agenda y introduce 6 contactos"""
    conexion.cursor().execute("delete  from contactos where 1 = 1")
    conexion.cursor().execute("insert into contactos values(%s, %s)", ("Juan", "666666666",))
    conexion.cursor().execute("insert into contactos values(%s, %s)", ("Pepe", "444455554",))
    conexion.cursor().execute("insert into contactos values(%s, %s)", ("Luis", "343423423",))
    conexion.cursor().execute("insert into contactos values(%s, %s)", ("Maria","233435962",))
    conexion.cursor().execute("insert into contactos values(%s, %s)", ("Hector","223322332",))
    conexion.commit()

def conexion(usu, pas):
    """
    Establece la conexion con la agenda
    :param usu: nombre de la base de datos en formato string
    :param pas: contraseña de la base de datos en formato string
    :return: devuelve False si no es puede establecer la conexion
    """
    """
    :param usu: recibe usuario en string
    :param pas: recibe una contraseña en string
    :return: devuelve la conexion y si no false
    """
    try:
        con = pymysql.connect("localhost", usu, pas, "agenda")
        return con
    except pymysql.err.OperationalError:  # error de conexion
        return False
    except RuntimeError:  # error en la contraseña
        return False


def agrega_contacto(telefono, conexion, nombre=None):
    """
    :param nombre: string del nombre a agregar
    :param telefono: string del telefono a agregar
    :param cursor: cursor de la conexion
    :return: void
    """
    if nombre == None:
        nombre = input("Introduzca un nombre:")
    try:
        conexion.cursor().execute("insert into contactos values(%s, %s)", (nombre, telefono,))
        conexion.commit()
        print("{} ha sido agregado correctamente".format(nombre))
    except pymysql.err.IntegrityError:
        print("{} no se ha podido agregar porque existe\nYa un contacto con este nombre".format(nombre))


def elimina_contacto(conexion, nombre):
    """
    :param conexion: recibe la conexion a la base de datos
    :param nombre: recinbe un string del nombre
    :return: elimina el registro con el nombre
    """
    cursor = conexion.cursor()
    cursor.execute("delete from contactos where nombre = (%s)", (nombre,))
    print("se han borrado un total de {} contactos".format(cursor.rowcount))
    conexion.commit()


def modifica_contacto(conexion, nombre, t):
    """
    es una funcion void no devuelve nada imprime para informar
    pero realmente lo que hace es modificar el telefono de un contacto de la agenda
    :param conexion: recibe la conexion
    :param nombre: recibe un string del nombre que se quiere modificat
    :param t: recibe el nuevo telefono a cambiar
    :return:  void no devuelve nada
    """
    if es_numero(t) and comprueba_contacto(conexion.cursor(), nombre):
        conexion.cursor().execute("update contactos set telefono=%s where nombre=%s", (t, nombre,))
        conexion.commit()
        print("Se le ha asignado a {} el teléfono {}".format(nombre, t))

    else:
        print("El telefono introducido no es correcto")



def muestra_contacto(cursor, texto=None):
    """ Muestra los contactos """
    sql = "Select * from contactos"
    datos = tuple()

    if texto != None:
        sql += " where nombre like %s"
        texto = "%" + texto + "%"
        datos = (texto,)

    cursor.execute(sql, datos)
    print("Hay un total de {} contactos".format(cursor.rowcount))  # cuenta las filas
    print()
    for (nombre, telefono) in cursor:
        print("{} : {}".format(nombre, telefono))


def es_numero(t):
    """Comprueba si la entrada del telefono es correcta"""
    try:
        int(t)
        return 6 < len(str(t)) < 15
    except ValueError:
        return False


def comprueba_contacto(cursor, n):
    """Comprueba si existe o no el usuario en la agenda"""
    cursor.execute("select * from contactos where 1 = 1")
    for (nombre, telefono) in cursor:
        if n == nombre:
            return True
    return False


def vacia_agenda(cursor):
    """
    :param cursor: recibe el cursor
    :return: devuelve un string en el que se indica el resultado
    de la accion de borrarlo todo
    """
    cursor.execute("delete  from contactos where 1 = 1")
    if cursor.rowcount >= 1:
        print("\nLa agenda se ha vaciado.\n " \
              "Ha eliminado {} registros".format(cursor.rowcount))
    else:
        print("La agenda está vacia")




