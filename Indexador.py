# Modulo indexador
# Proyecto final
# Recuperacion de la informacion y busqueda en web

from Lematizador    import Lematizador
from Transacciones  import ModuloTransacciones
from LSI            import IndiceLSI
from datetime       import datetime
from os             import system
from Consultas      import Consultas

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
            campos = archivo.read().split("\n<!campo>\n")

            # Insertar documento en la base de datos
            id = self.__moduloTransacciones.insertarDocumento( 
                campos[0], campos[1], campos[2][:508] + "...", campos[3], campos[4], 
                campos[5], campos[6], campos[7], campos[8] 
            ) # End insertar documento

            # Notificar registro en la base de datos
            print(("[!] Documento %s registrado en la base de datos con id: %s") % ( documento, id ))

            # Lematizar textos
            textoLematizado = self.__lematizador.lematizarTexto( campos[9] )
            
            # Cargar terminos de indexacion a la BD y registrar sus apariciones
            for posicion, palabra in enumerate(textoLematizado.split(" ")):

                # Revisar si la palabra tiene alguna relacion para lematizar
                # si no, pasarla directamente como termino

                termino = palabra
                self.__moduloTransacciones.insertarTermino(termino)
                self.__moduloTransacciones.registrarAparicion(id, termino, posicion)
                
            print(("[!] Documento %s lematizado e indexado correctamente") % (id))

        # Fabricar el LSI
        Consultas.establecerLSI()

        print("[!] Indexacion completada")
        input()