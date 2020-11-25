-- Drop si existe la base de datos
DROP DATABASE IF EXISTS Recuperador;
CREATE DATABASE Recuperador;
USE Recuperador;

-- Tabla para representar documentos
CREATE TABLE DOCUMENTO( id          INTEGER         NOT NULL,
                        autor       VARCHAR(255)    NOT NULL,
                        abstract    MEDIUMTEXT      NOT NULL,
                        fecha       DATE            NOT NULL,
                        editorial   VARCHAR(100)    NOT NULL,
                        lugar       VARCHAR(100)    NOT NULL,
                        revista     VARCHAR(255)    NOT NULL,
                        isbn        VARCHAR(30)     NOT NULL,
                        doi         VARCHAR(255)    NOT NULL,

                        PRIMARY KEY (id) );

-- Tabla para representar terminos de indexacion
CREATE TABLE TERMINO (  nombre VARCHAR(50) NOT NULL,
                        PRIMARY KEY (nombre) );

-- Tabla para representar palabras sin lematizacion
CREATE TABLE PALABRA (  nombre VARCHAR(50)  NOT NULL,
                        PRIMARY KEY (nombre) );

-- Tabla para representar relacion de aparicion entre documento y termino
CREATE TABLE APARECE (  documento   INTEGER         NOT NULL,
                        termino     VARCHAR(50)     NOT NULL,
                        posicion    INTEGER         NOT NULL,

                        FOREIGN KEY (documento) REFERENCES DOCUMENTO (id),
                        FOREIGN KEY (termino)   REFERENCES TERMINO (nombre),
                        PRIMARY KEY (documento, termino, posicion) );

-- Tabla para representar relacion de representacion entre termino y palabra
CREATE TABLE REPRESENTA (   palabra     VARCHAR(50)     NOT NULL,
                            termino     VARCHAR(50)     NOT NULL,

                            FOREIGN KEY (palabra) REFERENCES PALABRA (nombre),
                            FOREIGN KEY (termino) REFERENCES TERMINO (nombre),
                            PRIMARY KEY (palabra, termino) );