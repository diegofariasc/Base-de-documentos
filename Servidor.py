# Servidor para atender consultas
# Proyecto final
# Recuperacion de la informacion y busqueda en web
from json           import loads, dumps
from http.server    import BaseHTTPRequestHandler
from Transacciones  import ModuloTransacciones
from Consultas      import Consultas

class Servidor(BaseHTTPRequestHandler):

    __moduloTransacciones = ModuloTransacciones()
    __moduloConsultas = Consultas()

    def do_GET(self):

        try:

            nombreArchivo, extension = self.path[1:].split(".")

            self.send_response(200)
            self.send_header('Content-type', 'text/' + extension)
            self.end_headers()

            # Abrir archivo y leer bytes
            archivo = open( nombreArchivo + "." + extension , "rb" ) 
            contenido = archivo.read()
            archivo.close()
            self.wfile.write( contenido )

        except:
            pass
            

    def do_POST(self):

        # Parsear datos recividos y parsearlos a un diccionario de python
        longitud = int(self.headers["Content-Length"])
        datosJSON = loads( self.rfile.read(longitud).decode("utf-8") )
        datos = dict(datosJSON)

        # Establecer parametros del modulo de consultas
        Servidor.__moduloConsultas.setResultadosDevueltos(datos["resultados"])
        Servidor.__moduloConsultas.setMedidaProximidad(datos["proximidad"])
        Servidor.__moduloConsultas.setSeparaciones(datos["separacion"])

        # Establecer tipo de indice a usar 
        if datos["usarFreqT"]:
            Servidor.__moduloConsultas.setIndiceUsado( Consultas.TABLA_FRECUENCIAS )
        else:
            Servidor.__moduloConsultas.setIndiceUsado( Consultas.INDICE_LSI )

        respuesta, tiempo = Servidor.__moduloConsultas.consultar(datos["palabras"])

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write( bytes ( dumps( {"resultados" : respuesta, "tiempo" : tiempo} ), 'utf-8') )

