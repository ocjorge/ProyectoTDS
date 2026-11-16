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
        return handler()

    #--- casillas estadisticas
    def redibujar(e = None):
        elegidos = [(nombre, f) for (nombre, f), cb in zip(estadisticos.ESTADISTICOS, casillas) if cb.value]
        titulo.value = "Estadísticas seleccionadas: " + ", ".join(nombre for nombre, f in elegidos)
        if not elegidos:
            imagen.visible = False
            mensaje.value = "marca una o mas casillas para ver estadisticas"
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

    casillas = [ft.Checkbox(label=nombre, on_change=redibujar) for nombre, _ in estadisticos.ESTADISTICOS]

    def desmarcar_todo(e):
        for cb in casillas:
            cb.value = False
        redibujar()

    def boton(texto, on_click):
        return ft.ElevatedButton(texto, on_click=on_click, width=260)

    menu_bd = ft.Column([
        ft.Text("Base de datos", size=18, weight=ft.FontWeight.BOLD),
        ruta_csv,
        boton("Cargar CSV", accion_bd("Cargar CSV", lambda: accion_cargar_csv(ruta_csv.value))),
        boton("Transferir a Mongo", accion_bd("Transferir a Mongo", accion_transferir_mongo)),
        boton("Crear base de datos MySQL", accion_bd("Crear base de datos MySQL", sql_db.crear_bd)),
        boton("Crear tabla MySQL", accion_bd("Crear tabla MySQL", sql_db.crear_tabla)),
        boton("Insertar datos", accion_bd("Insertar datos", accion_insertar)),
    ], spacing=8)

    menu_est = ft.Column([
        ft.Text("Estadisticos", size=18, weight=ft.FontWeight.BOLD),
        *casillas,
        ft.TextButton("Desmarcar todo", on_click=desmarcar_todo),
    ], spacing=2)

    menu_sobre = ft.Column([
        ft.Text("Sobre", size=18, weight=ft.FontWeight.BOLD),
        ft.Text("Sistema de control de pasajeros 'Titanic'"),
        ft.Text("Jorge Ortiz"),
        ft.Text("Omar Martinez"),
        ft.text("Ramon Castillo"),
    ], spacing=2)


    panel_izq = ft.Column([menu_bd, ft.Divider(height=25), menu_est], width=290, scroll=ft.ScrollMode.AUTO)
    panel_der = ft.Column([titulo, mensaje, imagen], expand=True, scroll=ft.ScrollMode.AUTO, spacing=12)

    page.add(ft.Row([panel_izq, ft.VerticalDivider(width=1), panel_der], expand=True))


if __name__ == "__main__":
    ft.app(target=main)










