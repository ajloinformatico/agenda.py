import pymysql
from funciones import *

if __name__ == "__main__":

    print("""
        ############
        #  AGENDA  #
        ############
        """)
    print("Introduzca su nombre y contraseña para establecer conexion")
    nombre = input("Nombre:\n>>> ")
    contraseña = input("Contraseña:\n>>> ")

    if not conexion(nombre, contraseña):
        print("Usuario o contraseña no validos")
        exit()

    conexion = conexion(nombre, contraseña)
    cursor = conexion.cursor()
    print("Bienvenido " + nombre)
    crea_lista_simple(conexion) # crea una lista inicial
    conexion.commit()
    comandos = "\nIntroduzca un comando entre la lista:\n * fin\t * consulta\n * alta\t * " \
               "alta nombre\n * borra nombre\t * vacia agenda\n * modifica nombre\t * comandos"
    error_comando = "\nEl comando no es reconocido por el sistema. Inserte\n>>> comandos" # control de error xomando no existe
    print(comandos)
    while True:
        comando = input("\n>>> ")

        if len(comando.split()) == 1:
            if comando == "fin":
                vacia_agenda(cursor) # vacia la agenda
                conexion.commit()
                conexion.close()  # cierra conexion
                print("Hasta otra " + nombre)
                exit()

            elif comando == "comandos":
                print(comandos)

            elif comando == "alta":
                n = input("Introduzca el nombre del contacto:\n>>> ")
                t = input(f"Introduzca un telefono para {n}:\n>>> ")
                if es_numero(t):
                    print()
                    agrega_contacto(t, conexion, n)
                    muestra_contacto(cursor)  # muestra
                else:
                    print("\nEl teléfono introdcido no es válido")

            elif comando == "consulta":
                texto = input("Introduzca un parámetro para de busqueda:\n>>> ")
                muestra_contacto(cursor, texto)
            else:
                print(error_comando)

        elif len(comando.split()) == 2:
            if comando.split()[0] == "alta" and type(comando.split()[1]) == str:
                t = input(f"introduzca un telefono para {comando.split()[1]}:\n>>> ")
                if es_numero(t):
                    agrega_contacto(t, conexion, comando.split()[1])
                    muestra_contacto(cursor)  # muestra
                else:
                    print("\nEl teléfono introducido no es valido")

            elif comando.split()[0] == "borra" and type(comando.split()[1]) == str:
                if comprueba_contacto(cursor, comando.split()[1]):
                    elimina_contacto(conexion, comando.split()[1])
                    muestra_contacto(cursor)  # muestra
                else:
                    print(f"El usuario {comando.split()[1]} no existe en la agenda")

            elif comando.split()[0] == "modifica" and type(comando.split()[1]) == str:
                if comprueba_contacto(cursor, comando.split()[1]):
                    t = input("Introduzca un numero para {}:\n>>> ".format(comando.split()[1]))
                    modifica_contacto(conexion, comando.split()[1], t)
                    muestra_contacto(cursor)  # muestra
                else:
                    print(f"El usuario {comando.split()[1]} no existe en la agenda")

            elif comando.split()[0] == "vacia" and comando.split()[1] == "agenda":
                vacia_agenda(cursor)
                conexion.commit()

            else:
                print(error_comando)

        else:
            print(error_comando)
