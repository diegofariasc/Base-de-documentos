# Modulo lematizador de textos
# Proyecto final
# Recuperacion de la informacion y busqueda en web

from ColeccionesPalabras    import stopwords, sufijos
from re                     import sub

class Lematizador:

    """
    El metodo indica si una palabra es stopword
    Input:  (str) palabra con la palabra a verificar
    Output: (boolean) indicando si la palabra es stopword o no
    """
    def esStopword( self, palabra ):
        return  palabra in stopwords or \
                palabra.isnumeric()

    def lematizarTexto( self, texto ):

        lematizado = ""

        # Iterar sobre las lineas del documento
        for linea in texto:

            # Preprocesar linea
            linea = self.__preprocesarLinea( linea )

            # Hacer split si es un signo de puntuacion o espacio
            for palabra in linea.split():

                lematizado += self.__lematizarPalabra( palabra ) 

            # Agregar salto de linea al final para mantenerlas pese a la iteracion for
            lematizado +="\n"

        return lematizado


    def __lematizarPalabra( self, palabra):

        if self.esStopword(palabra) or len(palabra) < 3:
            return ""

        palabra = self.__removerSufijos( palabra )

        return palabra + " "


    """
    La funcion preprocesa una linea antes de ser lematizada y la devuelve
    sin signos gramaticales y en minusculas
    Input:  (str) con una linea del texto
    Output: (str) con la linea procesada
    """
    def __preprocesarLinea( self, linea ):

        # Pasar a minuscula
        linea = linea.lower()

        # Sustraer elementos de puntuacion
        linea = sub(r'(e-)', 'e', linea)
        linea = sub(r'[-/]', ' ', linea)
        linea = sub(r'[^\w\s]', '', linea)

        return linea

    """
    El metodo remueve los sufijos de una palabra empleando la coleccion
    del archivo ColeccionesPalabras.py
    Input:  (str) palabra con la plabra a la que se le pretenden eliminar sufijos
    Output: (str) con la palabra sin sufijos
    """
    def __removerSufijos( self, palabra ):

        # Verificar si la palabra coincide con algun sufijo
        for sufijo in sufijos:
            if ( palabra.endswith(sufijo) ):

                # Si es asi, removerlo
                return palabra[ : len(palabra) - len(sufijo) ] + sufijos[sufijo]

        # Regresar palabra original si no hay coincidencia
        return palabra


