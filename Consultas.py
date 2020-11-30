
from Transacciones  import ModuloTransacciones
from Lematizador    import Lematizador
from LSI            import IndiceLSI
from time           import time
from datetime       import datetime
from os             import system
import Proximidad   as p

class Consultas:

    # Constantes
    TABLA_FRECUENCIAS = 1
    INDICE_LSI = 2

    # Variables estaticas
    indiceLSI = None

    # Constructor
    def __init__( self ):

        self.__lematizador = Lematizador()
        self.__moduloTransacciones = ModuloTransacciones()
        self.__medidaProximidad = p.euc
        self.__resultadosDevueltos = 3
        self.__separacion = ""
        self.__indiceUsado = Consultas.TABLA_FRECUENCIAS

    # Coleccion de setters
    def setResultadosDevueltos ( self, cantidad ):
        self.__resultadosDevueltos = cantidad

    def setIndiceUsado ( self, indice ):
        self.__indiceUsado = indice

    def setSeparaciones ( self, separaciones ):
        self.__separaciones = separaciones

    def setMedidaProximidad ( self, nombre ):

        if nombre == "Producto interno":
            self.__medidaProximidad = p.euc

        if nombre == "Similitud de cosenos":
            self.__medidaProximidad = p.cos

        if nombre == "Coeficientes de Dice":
            self.__medidaProximidad = p.dice

        if nombre == "Coeficientes de Jaccard":
            self.__medidaProximidad = p.jacc

        if nombre == "Distancia euclidiana":
            self.__medidaProximidad = p.euc

        if nombre == "Distancia Manhattan":
            self.__medidaProximidad = p.manh

    
    @staticmethod
    def establecerLSI():

        # Recuperar la tabla de frecuencias 
        freqT = ModuloTransacciones().obtenerTablaDeFrecuencias()
        
        # Mostrar dimensiones de la tabla y las condiciones de la SVD
        M, N, R = IndiceLSI.mostrarDimensionesSVD( freqT )
        print("\n-> Generador de indices LSI ")
        print(("\n[!] La matriz de frecuencias tiene actualmente la forma : M = %s x N = %s") % (M,N)) 
        print(("[!] La descomposicion SVD resulta en : T=(%sx%s), S=(%sx%s), DT=(%sx%s)\n") % (M,R,R,R,N,R)) 
        k = int ( input("-> Establezca una reduccion de R a K = ") )

        Consultas.indiceLSI = IndiceLSI(freqT,k)

        print("[!] Indice LSI generado correctamente", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        input("Enter para continuar...")


    """
    El metodo permite plantear una consulta 
    usuario experto
    Input:  None
    Output: None
    """
    def __plantearConsulta( self, texto ):

        # Lematizar textos
        textoLematizado = self.__lematizador.lematizarTexto( texto )

        # Plantear consulta en la base de datos
        id = self.__moduloTransacciones.generarConsulta()

        # Cargar terminos de indexacion a la BD y registrar sus apariciones
        for posicion, palabra in enumerate(textoLematizado.split(" ")):

            # Revisar si la palabra tiene alguna relacion para lematizar
            # si no, pasarla directamente como termino

            termino = palabra
            self.__moduloTransacciones.registrarAparicion(id, termino, posicion) 

        return id


    def __obtenerIdDocumentosDevolver ( self, texto ):

        idConsulta = self.__plantearConsulta( texto )


        # if consultar en el indice normal o el lsi

        vectorConsulta = self.__moduloTransacciones.obtenerVectorDocumento(idConsulta)
        numeroDocumentos = self.__moduloTransacciones.obtenerMaximoIdDocumentos() + 1

        # Calcular distancias 
        distancias = [ (self.__medidaProximidad( 
                        self.__moduloTransacciones.obtenerVectorDocumento(id), vectorConsulta ), id)  
                        for id in range( numeroDocumentos ) ]

        distancias.sort()

        # Revisar si la medida es de disimilitud
        if ( self.__medidaProximidad in {p.innerprod, p.cos, p.dice, p.jacc} ):
            distancias.reverse()


        # Al terminar, sacar la consulta de la BD
        self.__moduloTransacciones.eliminarConsulta(idConsulta)

        # Extraer ids unicamente
        idsResultado = [ id for proximidad, id in distancias ]
        return idsResultado[:self.__resultadosDevueltos]


    def __consultarLSI( self, texto ):

        # Plantear consulta en el dominio de FreqT
        idConsulta = self.__plantearConsulta( texto )
        Q = self.__moduloTransacciones.obtenerVectorDocumento(idConsulta)

        # Solicitar al indice LSI la transformacion de la consulta y la busqueda en el indice
        resultados = Consultas.indiceLSI.consultar(Q, self.__medidaProximidad, self.__resultadosDevueltos)

        # Eliminar planteamiento de consulta de la base de datos
        self.__moduloTransacciones.eliminarConsulta(idConsulta)
        return resultados


    def consultar ( self, texto ):

        metodo = None
        if self.__indiceUsado == Consultas.INDICE_LSI:
            metodo = self.__consultarLSI
        else:
            metodo = self.__obtenerIdDocumentosDevolver

        inicio = time()
        return ([self.__moduloTransacciones.obtenerInformacionDocumento(id) 
                for id in metodo(texto)], time() - inicio)


