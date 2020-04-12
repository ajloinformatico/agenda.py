import pytest
from funciones import *

# introduzca su nombre  y contraseña correctos para la base de datos
# asegurate de tener encendido el servidor y ejecuta los text
nombre_co = "pepito"
contraseña_co = "grillo"
con = conexion(nombre_co, contraseña_co)
cursor = con.cursor()




def test_conexion():
    assert conexion("nombre_erroneo", "contraseña_cualquiera") == False
    assert conexion(nombre_co, contraseña_co)


def test_crea_lista_simple():
    """comprueba si se han agregado los 5 registros"""
    crea_lista_simple(con)
    cursor.execute("select * from contactos")
    assert cursor.rowcount == 5

def test_vacia_agenda():
    """comprueba si se vacia la agenda"""
    vacia_agenda(cursor)
    cursor.execute("select * from contactos")
    assert cursor.rowcount == 0
    con.commit()
    crea_lista_simple(con)

def test_comrpueba_contacto():
    """Comprueba si el contacto existe"""
    assert comprueba_contacto(cursor, "pepe") == False
    assert comprueba_contacto(cursor, "Juan") == True

def test_es_numero():
    """Comprueba que el numero se ha introducido correctamente"""
    assert es_numero("78") == False # no cumple con la longitud minima
    assert es_numero("1234epwe3") == False # no es un numero
    assert es_numero("956665655") == True

def test_modifica_contacto():
    """Comprueba que se modifica correctamente el contacto"""
    def comprueba_telefono(nombre_busqueda):
        """Busca el telefono del nombre introducido
        Funcion para reducir codigo del test modifica_contacto"""
        datos = tuple()
        cursor.execute("Select * from contactos", datos)
        for (nombre, telefono) in cursor:
            print("{} : {}".format(nombre, telefono))
            if nombre == nombre_busqueda:
                return telefono

    # busca el telefono de juan
    telefono_antiguo = comprueba_telefono("Juan")
    # nos aseguramos de que es el mismo que habia antes
    assert telefono_antiguo == "666666666"
    # Se modifica el numero del contacto de juan
    modifica_contacto(con, "Juan", "956777667")
    # busca el telefono nuevo que se le ha dado a juan
    telefono_nuevo = comprueba_telefono("Juan")
    # comprueba que efectivamente se le ha cambiadop el telefono a juan
    assert telefono_nuevo == "956777667"
    # por ultimo comprobamos quie le telefono nuevo es distinto que el telefono antiguo
    assert telefono_antiguo != telefono_nuevo

def test_elimina_contacto():
    # comprueba que el contacto pepe previamente existe
    assert comprueba_contacto(cursor, "Pepe") == True
    # elimno el contacto
    elimina_contacto(con, "Pepe")
    # Ya pepe no existe
    assert comprueba_contacto(cursor, "Pepe") == False

def test_agrega_contacto():
    # El contacto previamente no existe
    assert comprueba_contacto(cursor, "Elena") == False
    agrega_contacto("956556677", con, "Elena")
    assert comprueba_contacto(cursor, "Elena") == True
