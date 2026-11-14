import os

import flet as ft

import estadisticos
import mongo_db
import sql_db
import validacion

CSV_POR_DEFECTO = "titanic.csv"

ESTADO = {"datos": []}  # datos cargados del CSV, compartidos entre botones




