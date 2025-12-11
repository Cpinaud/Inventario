import sqlite3
database = "inventary.db"

def connect():
    '''
    Inicia la coneción con la base de datos

    :return: cursor y connection para el manejo de la base
    '''
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    return connection,cursor

def execute(cursor,query,connection,params=""):
    '''
    Ejecuta las sentencias a la base de datos recibiendo por
    parámetros toda la información necesaria
    
    :param cursor: cursor de la conexión, creado en connect()
    :param query: sentencia a ejecutar
    :param connection: conexión a la base, creado en connect()
    :param params: parámetros de la sentencia
    '''
    cursor.execute(query,params)
    connection.commit()   

def select(cursor):
    '''
    Devuelve el resultado de una sentencia select
    
    :param cursor: cursor de la conexión, creado en connect()
    '''
    return cursor.fetchall()

def close(connection):
    '''
    Cierra conexión con la base de datos
    
    :param connection: conexión a la base, creado en connect()
    '''
    connection.close()    