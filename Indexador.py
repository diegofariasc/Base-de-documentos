# Modulo indexador
# Proyecto final
# Recuperacion de la informacion y busqueda en web

from Lematizador    import Lematizador
from Transacciones  import ModuloTransacciones
from LSI            import IndiceLSI
from datetime       import datetime
from os             import system

class Indexador:

    # Constructor
    def __init__( self ):

        self.__lematizador = Lematizador()
        self.__moduloTransacciones = ModuloTransacciones()
        
    """
    El metodo permite indexar una coleccion de documentos 

    """
    def indexar( self, documentos ):

        system("clear")
        print("[!] Inicio del proceso de indexacion", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        # Por cada documento en la coleccion
        for documento in documentos:

            # Cargar el documento y enviarlo a lematizar
            archivo = open( documento , "r")
            print(self.__lematizador.lematizarTexto( archivo ))

        print("[!] Indexacion completada")
        input()