import mysql.connector

class ModuloTransacciones:

    # Constructor
    def __init__( self ):

        self.__connection = mysql.connector.connect(    
            user="root", 
            password="password", 
            host="127.0.0.1",
            database="Recuperador" 
        ) # End connect


    # -----------------------------------------------------------------
    # METODOS DE INSERCION
    # -----------------------------------------------------------------

    """
    El metodo permite ejecutar una serie de operaciones en la base de datos
    Input:  (list of string) con la lista de operaciones a ejecutar
    Output: (boolean) indicando si se ha completado la lista de operaciones
    """
    def __ejecutar( self, operaciones ):

        try:

            # Obtener cursor
            cursor  = self.__connection.cursor()

            # Ejecutar la lista de operaciones solicitada
            for instruccion in operaciones:
                cursor.execute( instruccion )

            # Al concluir la lista de operaciones hacerlas permanentes
            self.__connection.commit()

        except:

            # En caso de error -> rollback
            self.__connection.rollback()
            cursor.close()
            return False


    """
    El metodo permite obtener el maximo id presente entre la coleccion
    de documentos
    Input:  None
    Output: (int) con el numero del mayor indice
    """
    def obtenerMaximoIdDocumentos( self ):
        
        # Obtener el maximo id de la tabla DOCUMENTO
        cursor = self.__connection.cursor()
        query = "SELECT MAX(id) FROM DOCUMENTO"
        cursor.execute( query )
        resultado = cursor.fetchall()

        # Verificar si aun no hay ninguna insercion
        # Si es asi, devolver el indice -1. De otra forma, devolver el indice maximo
        if ( resultado[0][0] == None ):
            return -1
        else:
            return resultado[0][0]

    """
    El metodo permite insertar un termino de indexacion 
    Input:  (str) terminoIndexacion con el termino a agregar
    Output: (bool) indicando si la transaccion fue exitosa
    """
    def insertarTermino( self, terminoIndexacion ):

        # Ejecutar insercion
        instruccion = ("INSERT INTO TERMINO ( nombre ) VALUES ('%s')")\
        % ( terminoIndexacion )

        self.__ejecutar([instruccion])


    """
    El metodo permite insertar un termino de indexacion 
    Input:  (str) palabra con la palabra a agregar
    Output: (bool) indicando si la transaccion fue exitosa
    """
    def insertarPalabra( self, palabra ):

        # Ejecutar insercion
        instruccion = ("INSERT INTO PALABRA ( nombre ) VALUES ('%s')") % ( palabra )
        self.__ejecutar([instruccion])


    """
    El metodo permite insertar una relacion entre una palabra y su termino
    Input:  (str) palabra y termino con la palabra y termino a relacionar
    Output: (bool) indicando si la transaccion fue exitosa
    """
    def insertarRelacionPalabraTermino( self, palabra, termino ):

        # Ejecutar insercion
        instruccion = ("INSERT INTO REPRESENTA ( palabra, termino ) VALUES ('%s', '%s')")\
        % ( palabra, termino )
        self.__ejecutar([instruccion])


    """
    El metodo permite insertar un documento en la base de datos
    Input:  (str) autor, abstract, fecha, editorial, lugar, revista, isbn, doi 
            con la informacion del documento que se pretende insertar
    Output: (int) con el id del documento insertado en caso exitoso. De lo contrario None
    """
    def insertarDocumento( self, autor, abstract, fecha, editorial, lugar, revista, isbn, doi ):

        try:

            # Obtener el maximo id presente en la tabla de documentos
            id = self.obtenerMaximoIdDocumentos() + 1

            # Preparar insercion 
            instruccion = ("INSERT INTO DOCUMENTO ( id, autor, abstract, fecha, editorial, lugar, revista, isbn, doi )\
            VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')")\
            % ( id, autor, abstract, fecha.strftime('%Y-%m-%d'), editorial, lugar, revista, isbn, doi )

            # Ejecutar insercion
            cursor = self.__connection.cursor()
            cursor.execute( instruccion )
            self.__connection.commit()
            return id
            
        except:

            # En caso de error -> rollback
            self.__connection.rollback()
            cursor.close()
            return None

    """
    El metodo permite registrar la aparicion de un termino en un documento en
    una posicion determinada
    Input:  (str) palabra, termino y su posicion en el documento
    Output: (bool) indicando si la transaccion fue exitosa
    """
    def registrarAparicion( self, documento, termino, posicion ):

        # Ejecutar insercion
        instruccion = ("INSERT INTO APARECE ( documento, termino, posicion ) VALUES (%s, '%s', %s)")\
        % ( documento, termino, posicion )
        self.__ejecutar([instruccion])

    # -----------------------------------------------------------------
    # METODOS DE RECUPERACION
    # -----------------------------------------------------------------

    """
    El metodo permite recuperar el vector representativo de un documento
    mediante una consulta a la base de datos
    Input:  (int) con el numero de documento que se desea
    Output: (list of int) con el vector de frecuencias de cada termino (ordenado asc)
    """
    def obtenerVectorDocumento( self, id ):

        try:

            cursor = self.__connection.cursor()
            query = "SELECT conteo FROM " +\
                    "(SELECT * FROM " +\
                    "((SELECT termino, COUNT(*) conteo FROM APARECE " +\
                    ("WHERE documento = %s ") % (id) +\
                    "GROUP BY termino) " +\
                    "UNION " +\
                    "(SELECT nombre, 0 from TERMINO " +\
                    "WHERE nombre NOT IN " +\
                    "(SELECT DISTINCT termino FROM APARECE " +\
                    ("WHERE documento = %s ))) frecuencias ") % (id) +\
                    "ORDER BY termino asc) ordenada"
                        
            cursor.execute( query )
            resultado = [ count[0] for count in cursor.fetchall() ] 
            return resultado

    
        except:

            # En caso de error -> rollback
            self.__connection.rollback()
            cursor.close()
            return None


    """
    El metodo constituye una tabla de frecuencias a partir de la informacion almacenada
    en la base de datos
    Input:  None
    Output: (list of list of int) con la tabla de frecuencias
    """
    def obtenerTablaDeFrecuencias( self ):

        numeroDocumentos = self.obtenerMaximoIdDocumentos()
        tabla = []

        # Iterar sobre todos los ids de documentos
        for documento in range( numeroDocumentos + 1):
            
            # Recuperar el enesimo vector columna de la tabla 
            vector = self.obtenerVectorDocumento(documento)
            
            # Verificar si no es nulo en caso de eliminaciones
            if (vector != None):
                tabla.append(vector)

        return tabla
        


