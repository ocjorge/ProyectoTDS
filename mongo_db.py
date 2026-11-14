from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "titanic_db"
MONGO_COL = "pasajeros"

def _coleccion():
    """Devuelve la colección de MongoDB"""
    cli = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    return cliente[MONGO_DB][MONGO_COL]

def transferir(datos):
    """Guarda la lista de diccionarios en MongoDB
    reemplaza la anterior colección (si existe)"""
    if not datos:
        raise ValueError("No hay datos para transferir.")
    col = _coleccion()
    col.delete_many({})  # borrar todo lo que haya antes
    col.insert_many([dict(d) for d in datos])
    return f"{len(datos)} documentos guardados en MongoDB ({MONGO_DB}.{MONGO_COL})."

def leer():
    """ Devuelve todos los documentos de Mongo como lista de diccionarios"""
    docs = list(_coleccion()).find({}, {"_id": 0})  # no incluir el _id de Mongo
    if not docs:
        raise ValueError("No hay datos en MongoDB. Usa 'Transferir a MongoDB' primero.")
    return docs

