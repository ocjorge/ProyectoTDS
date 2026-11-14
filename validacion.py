"""Validacion con regex y carga del CSV."""
import csv
import os
import re


RE_ENTERO = re.compile(r"^\d+$")                    # 1, 25, 891
RE_NOMBRE = re.compile(r"^[^,]+,\s*[^.]+\.\s*.+$")  # "Apellido, Mr. Nombre"
RE_SEXO = re.compile(r"^(male|female)$")
RE_EDAD = re.compile(r"^\d{1,3}(\.\d+)?$")          # 22 o 22.5
RE_TARIFA = re.compile(r"^\d+(\.\d+)?$")            # 7.25
RE_PUERTO = re.compile(r"^[SCQ]$")                  # S, C o Q


def fila_valida(f):
    """Valida una fila del CSV según las reglas definidas.
        es true si todos los campos que usa cumplen con el regex
        datos vacions no pasan la validación"""
    return all([
        RE_ENTERO.match(f["PassengerId"].strip()),
        RE_ENTERO.match(f["Pclass"].strip()),
        RE_NOMBRE.match(f["Name"].strip()),
        RE_SEXO.match(f["Sex"].strip()),
        RE_EDAD.match(f["Age"].strip()),
        RE_TARIFA.match(f["Fare"].strip()),
        RE_PUERTO.match(f["Embarked"].strip()),
    ])


def cargar_csv(ruta):
    """Lee el CSV y devuelve solo las filas validas
    (una lista de dicts ya con tipos correctos)"""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    validas = []
    for r in filas:
        if fila_valida(r):
            validas.append({
                "id": int(r["PassengerId"]),
                "nombre": r["Name"].strip(),
                "sexo": r["Sex"].strip(),
                "clase": int(r["Pclass"]),
                "edad": float(r["Age"]),
                "tarifa": float(r["Fare"]),
                "puerto": r["Embarked"].strip(),
            })
    return validas, len(filas) - len(validas), len(filas)
