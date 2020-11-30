# Indice LSI
# Clase recuperada de la actividad 5
# Proyecto final
# Recuperacion de la informacion y busqueda en web

from math           import sqrt, inf
from numpy          import array, shape, dot, zeros, diag, allclose, append, transpose, round
from numpy.random   import randint
from numpy.linalg   import svd, inv, solve, qr, lstsq


"""
La clase representa un indice empleando Latent Semantic Indexing.
Permite cargar una matriz de frecuencias y realizarle consultas de documentos
dados vectores de peso de terminos
"""
class IndiceLSI:

    # Constructor
    def __init__( self, freqT, k ):

        self.establecerMatrizFrecuencias( freqT, k )

    """
    El metodo funge como setter para cambiar la matriz de frecuencias
    de la instancia, el parametro k y las matrices derivadas de su 
    descomposicion SVD: T*, S* y DT*
    Input:  freqT con la matriz de frecuencias de dimension (M x N)
            k con el numero de terminos significativos en S 
            que se conservaran
    Output: Matrices T*, S*, DT* con su dimensionalidad 
            (M x k), (k x k) y (k x N) respectivamente
    """
    def establecerMatrizFrecuencias(self, freqT, k ):

        self.__freqT =  freqT
        self.__k = k
        self.__Ts, self.__Ss, self.__DTs, self.__M, self.__N, self.__R = self.__reducir( freqT, k )

        # Establecer coeficientes
        self.__coef = self.__calcularCoeficientes()

    """
    El metodo reduce una matriz de frecuencias mediante la metodologia 
    SVD 
    """
    def __reducir( self, freqT, k ):

        # Hacer descomposicion SVD
        T, Sv, DT = svd( freqT , full_matrices=False)

        # Extraer dimensiones
        M = shape( T ) [0]
        N = shape( DT )[1]
        R = shape( T ) [1]

        # Aplicar recorte sobre el vector Sv y llevarlo a matriz
        Ss = diag ( Sv[:k] )

        # Aplicar recorte en DT y T
        DTs = DT[:k,:]
        Ts  = T[:,:k]

        return ( Ts, Ss, DTs, M, N, R )

    @staticmethod
    def mostrarDimensionesSVD( freqT ):
        
        # Hacer descomposicion SVD
        T, _, DT = svd( freqT , full_matrices=False)

        # Extraer dimensiones
        M = shape( T ) [0]
        N = shape( DT )[1]
        R = shape( T ) [1]

        return ( M, N, R )

    """
    El metodo calcula las soluciones de un sistema de ecuaciones
    donde el atributo de la tabla self.__coef son los coeficientes
    de las variables y Q o la consulta es el segundo miembro de la igualdad
    Input:  Q. Un numpy array en forma de vector con una consulta
    Output: Un numpy array con las soluciones del sistema de ecuaciones
    """
    def __calcularSoluciones(self, Q):

        # Calcular soluciones del sistema de ecuacion
        Qs = lstsq( self.__coef, Q, rcond=None)[0]

        return Qs

    """
    El metodo realiza una consulta sobre DT* y devuelve los dd
    documentos mas relevantes. Los documentos devueltos se encuentran
    organizados de acuerdo con su similitud
    Input:  Numpy array Q con los pesos de cada termino en consulta
            dd (opcional) el numero de documentos que se desea que sean devueltos
    Output: Lista con los numeros de documentos mas relevantes
    """
    def consultar(self, Q, funcion, dd = 1):

        # Obtener una lista de tuplas (similitud, consulta)
        similitudes = [(funcion( self.__DTs[:, doc],
                        self.__calcularSoluciones( Q ) ), doc)
                        for doc in range(self.__N)]

        # Organizar de acuerdo con la similitud
        similitudes.sort()

        # Extraer los indices de documentos con mayor similitud y ordenarlos
        resultados = [doc + 1 for _, doc in similitudes[:dd]]

        return resultados

    """
    El metodo calcula los coeficientes para un sistema de ecuaciones
    a partir de S* y T* 
    Input:  None
    Output: Numpy array (matriz de M x N) con los coeficientes del sistema 
            de ecuaciones
    """
    def __calcularCoeficientes(self):

        # Crear matriz de 0s
        coef = zeros( (self.__M, self.__k) )

        # Iterar M y k para construit T*S*,...
        for i in range( self.__M ):
            for j in range( self.__k ):
                coef[i,j] = self.__Ts[i,j] * self.__Ss[j,j]

        return coef




