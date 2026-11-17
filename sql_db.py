import mysql.connector
import numpy as np

MYSQL_CFG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306,
}
MYSQL_DB = "titanic"
MYSQL_TABLE = "pasajeros"

def _conectar(con_bd=True):
    if con_bd:
        return mysql.connector.connect(database = MYSQL_DB, **MYSQL_CFG) # Conectar a la base de datos
    return mysql.connector.connect(**MYSQL_CFG)

def crear_bd():
    """Crea la base de datos"""
    con = _conectar(con_bd=False)
    con.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} CHARACTER SET utf8mb4;")
    con.close()
    return f"Base de datos '{MYSQL_DB}' lista."

def crear_tabla():
    """Crea la tabla"""
    con = _conectar()
    con.cursos().execute(f"""
        CREATE TABLE IF NOT EXISTS {MYSQL_TABLE} (
            id INT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            sexo VARCHAR(10) NOT NULL,
            clase INT NOT NULL,
            edad FLOAT NOT NULL,
            tarifa DECIMAL(10,4) NOT NULL,
            puerto CHAR(1) NOT NULL
        )""")
    con.close()
    return f"Tabla '{MYSQL_TABLE}' lista."


def insertar(docs):
    """Inserta una lista de diccionarios (reemplaza lo que hubiera en la tabla)."""
    con = _conectar()
    cur = con.cursor()
    cur.execute(f"DELETE FROM {MYSQL_TABLE}")
    cur.executemany(
        f"INSERT INTO {MYSQL_TABLE} (id, nombre, sexo, clase, edad, tarifa, puerto) "
        f"VALUES (%s,%s,%s,%s,%s,%s,%s)",
        [(d["id"], d["nombre"], d["sexo"], d["clase"], d["edad"], d["tarifa"], d["puerto"])
         for d in docs])
    con.commit()
    con.close()
    return f"{len(docs)} registros insertados en MySQL."

def consultar():
    """Devuelve tres arreglos de NumPy: edades, puertos, tarifas."""
    con = _conectar()
    cur = con.cursor()
    cur.execute(f"SELECT edad, puerto, tarifa FROM {MYSQL_TABLE}")
    filas = cur.fetchall()
    con.close()
    if not filas:
        raise ValueError("La tabla MySQL esta vacia. Inserta datos primero.")
    edades = np.array([r[0] for r in filas], dtype=float)
    puertos = np.array([r[1] for r in filas])
    tarifas = np.array([float(r[2]) for r in filas])
    return edades, puertos, tarifas