import os

import flet as ft

import estadisticos
import mongo_db
import sql_db
import validacion

CSV_POR_DEFECTO = "titanic.csv"

ESTADO = {"datos": []}  # datos cargados del CSV, compartidos entre botones


#--- aciones del menu Base datos
def accion_cargar_csv(ruta):
    validas, descartas, total = validacion.cargar_csv(ruta)
    ESTADO["datos"] = validas
    return(f"CSV cargado: {os.path.abspath(ruta)}\n"
           f"Filas totales: {total}\n"
           f"filas válidas: {len(validas)}\n"
           f"filas descartadas: {len(descartas)}")


def accion_transferir_mongo():
    return mongo_db.transferir(ESTADO["datos"])

def accion_insertar():
    docs = mongo_db.leer()
    return sql_db.insertar(docs)

def main(page: ft.Page):
    page.title = "Sistema de control pasajeros 'Tintanic'"
    page.window.resizable = True
    page.window.maximizable = True
    page.window_width = 1300
    page.window_height = 760
    page.padding = 15
    page.Theme = ft.Theme(color_scheme_seed=ft.colors.BLUE_400, use_material3=True)


    titulo = ft.Text("Selecciona una opción del menú", size = 22, weight = ft.font_weight.BOLD, color = ft.colors.BLUE_900)
    mensaje = ft.Text("", size = 14, selectable = True)
    imagen = ft.Image(visible = false, fit = ft.ImageFit.CONTAIN)

    #--- botones del menu Base datos







