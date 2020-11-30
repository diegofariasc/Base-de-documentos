
# Interfaz por linea de comandos para el usuario experto 
# Proyecto final
# Recuperacion de la informacion y busqueda en web

from Indexador      import Indexador
from Servidor       import Servidor
from Consultas      import Consultas
from socketserver   import TCPServer
from os             import system
from datetime       import datetime


class InterfazExperto:


    """
    El metodo muestra el menu de opciones de la interfaz del 
    usuario experto
    Input:  None
    Output: None
    """
    def __mostrarMenuOpciones( self ):

        system("clear")
        print("Interfaz de usuario experto:")
        print("Que desea hacer ahora?\n")
        print("1. Indexar una coleccion de documentos")
        print("2. Iniciar servidor")
        print("3. Salir")


    """
    El metodo interpreta la seleccion del usuario de entre las opciones
    del menu principal de opciones e invoca a la funcion correspondiente 
    para atenderla
    Input:  None
    Output: None
    """
    def __interpretarSeleccion( self ):

        # Solicitar una seleccion por parte del usuario
        opcion = input("-> ")

        # El usuario elige indexar
        if opcion == "1":
            self.__procesarOpcionIndexar()

        # El usuario elige lanzar el servidor
        if opcion == "2":

            # Generar un indice LSI previo a lanzar el servidor
            if Consultas.indiceLSI == None:
                system("clear")
                print("\n[!] Debe generar un indice LSI antes de continuar...")
                Consultas.establecerLSI()

            system("clear")
            print("[!] Servidor de consultas iniciado", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print("[!] Utilice ctrl + C para terminar el servidor")
            httpd = TCPServer(("", 8080), Servidor)
            httpd.serve_forever()

        # Si el usuario elige salir
        elif opcion == "3":
            exit()

        else:
            print("\n[!] Opcion no valida")


    """
    El metodo despliega la interfaz para llevar a cabo el proceso
    de indexacion
    Input:  None
    Output: None
    """
    def __procesarOpcionIndexar( self ):

        
        # Imprimir instrucciones del indexador
        system("clear")
        print("Subsistema indexador:") 
        print("-> Indique el nombre de los archivos a indexar. Presione enter para finalizar")

        # Inicializar coleccion vacia de archivos a indexar
        archivosIndexar = []
        
        # Obtener los nombres de los archivos
        while True:

            # Si no se proporciona un nombre, terminar
            # Si se proporciona uno agregarlo a la coleccion
            archivo = input("-> ")
            if archivo == "":
                break
            else:
                archivosIndexar.append( archivo )

        # Confirmar la coleccion a indexar
        system("clear")
        print("\n-> Indexar", len(archivosIndexar), "documento(s): ")
        print("->", archivosIndexar)
        print("-> Confirma ?")
        print("-> 1. Si")
        print("-> 2. No")

        # Esperar a tener una seleccion valida
        while True:
            
            # Leer seleccion
            seleccion = input("-> ")
            
            # Interpretarla
            if seleccion == "1":
                self.__indexador = Indexador()
                self.__indexador.indexar( archivosIndexar )
                break

            if seleccion ==  "2":
                print("\n[!] Operacion de indexacion abortada")
                input()
                break


    """
    El metodo lanza la interfaz por linea de comandos 
    del sistema 
    Input:  None
    Output: None
    """
    def iniciar( self ):

        # Mantener activa la interfaz
        while True:
            
            # Desplegar opciones, obtener la seleccion e interpretarla
            self.__mostrarMenuOpciones()
            self.__interpretarSeleccion()


