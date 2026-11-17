import os

import flet as ft

import estadisticos
import mongo_db
import sql_db
import validacion

CSV_POR_DEFECTO = "titanic.csv"

ESTADO = {"datos": []}  # datos cargados del CSV, compartidos entre botones

ruta_csv = ft.TextField(label="Ruta del CSV", value=CSV_POR_DEFECTO, width=260)


#--- aciones del menu Base datos
def accion_cargar_csv(ruta):
    validas, descartadas, total = validacion.cargar_csv(ruta)
    ESTADO["datos"] = validas
    return(f"CSV cargado: {os.path.abspath(ruta)}\n"
           f"Filas totales: {total}\n"
           f"filas válidas: {len(validas)}\n"
           f"filas descartadas: {descartadas}")


def accion_transferir_mongo():
    return mongo_db.transferir(ESTADO["datos"])

def accion_insertar():
    docs = mongo_db.leer()
    return sql_db.insertar(docs)

def main(page: ft.Page):
    page.title = "Sistema de control pasajeros 'Tintanic'"
    page.window.resizable = True
    page.window.maximizable = True
    page.window.width = 1300
    page.window.height = 760
    page.padding = 15
    page.Theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_400, use_material3=True)


    titulo = ft.Text("Selecciona una opción del menú", size = 22, weight = ft.FontWeight.BOLD, color = ft.Colors.BLUE_900)
    mensaje = ft.Text("", size = 14, selectable = True)
    imagen = ft.Image(visible = False, fit = ft.ImageFit.CONTAIN)

    #--- botones del menu Base datos
    def accion_bd(nombre, funcion):
        def handler(e):
            titulo.value = nombre
            imagen.visible = False
            mensaje.value = "Procesando..."
            page.update()
            try:
                mensaje.value = funcion()
            except Exception as ex:
                mensaje.value = f"Error: {ex}"
            page.update()
        return handler

    #.. Estadisticos.
    marcados = [False] * len(estadisticos.ESTADISTICOS)
    items_est = []

    def redibujar():
        elegidos = [(n, f) for (n, f), m in zip(estadisticos.ESTADISTICOS, marcados) if m]
        titulo.value = "Estadisticos"
        if not elegidos:
            imagen.visible = False
            mensaje.value = "Marca uno o mas estadisticos en el menu"
            page.update()
            return
        try:
            edades, puertos, tarifas = sql_db.consultar()
            b64, resumen, cols = estadisticos.dibujar(elegidos, edades, puertos, tarifas)
            imagen.src_base64 = b64
            imagen.width = 480 if cols == 1 else 900
            imagen.visible = True
            mensaje.value = resumen
        except Exception as ex:
            imagen.visible = False
            mensaje.value = f"Error: {ex}"
        page.update()

    def icono(marcado):
        return ft.Icon(ft.Icons.CHECK_BOX if marcado else ft.Icons.CHECK_BOX_OUTLINE_BLANK)

    def alternar(i):
        def handler(e):
            marcados[i] = not marcados[i]
            items_est[i].leading = icono(marcados[i])
            redibujar()
        return handler

    for i, (nombre, _) in enumerate(estadisticos.ESTADISTICOS):
        items_est.append(ft.MenuItemButton(content=ft.Text(nombre), leading=icono(marcados[i]), on_click=alternar(i)))

    def desmarcar_todo(e):
        for i in range(len(marcados)):
            marcados[i] = FileExistsError
            items_est[i].leading = icono(False)
        redibujar()

    #Sobre
    def mostrar_sobre(e):
        titulo.value = "Sobre"
        imagen.visible = False
        mensaje.value = ("Sistema de control de pasajeros 'Titanic'\n\n"
                         "Jorge Ortiz\nOmar Martinez\nRamon Castillo")
        page.update()

    #barra de menu
    def item(texto, on_click):
        return ft.MenuItemButton(content=ft.Text(texto), on_click=on_click)

    barra = ft.MenuBar(controls=[
        ft.SubmenuButton(content=ft.Text("Base de datos"), controls=[
            item("Cargar CSV", accion_bd("Cargar CSV", lambda: accion_cargar_csv(ruta_csv.value))),
            item("Transferir a Mongo", accion_bd("Transferir a Mongo", accion_transferir_mongo)),
            item("Crear base de datos MySQL", accion_bd("Crear base de datos MySQL", sql_db.crear_bd)),
            item("Crear tabla MySQL", accion_bd("Crear tabla MySQL", sql_db.crear_tabla)),
            item("Insertar datos", accion_bd("Insertar datos", accion_insertar)),
        ]),
        ft.SubmenuButton(content=ft.Text("Estadisticos"), controls=[
            *items_est,
            item("Desmarcar todo", desmarcar_todo),
        ]),
        ft.SubmenuButton(content=ft.Text("Sobre"), controls=[
            item("Acerca de", mostrar_sobre),
        ]),
    ])
    contenido = ft.Column([ruta_csv, titulo, mensaje, imagen],
                          expand=True, scroll=ft.ScrollMode.AUTO, spacing=12)

    page.add(ft.Row([barra]), ft.Divider(height=1), contenido)

if __name__ == "__main__":
    ft.app(target=main)
