import base64 #se importa para convertir la imagen a base64
import io #se importa para crear un buffer de memoria
import math
""" 
Cada función dibuja sobre el eje X (ax) que recibe y devuelve un texto resumen.
El titanic no tiene pais ni idas de estancia:
pais se cambia por puerto de embarque definidos en main (S, C, Q) y 
estancia se cambia por tarifa pagada
"""

import matplotlib
matplotlib.use("Agg")  # sin ventana: la imagen se muestra dentro de Flet
import matplotlib.pyplot as plt
import numpy as np

PUERTOS = {
    "S": "Southampton",
    "C": "Cherburgo",
    "Q": "Queenstown"
}

def est_promedios(ax, e, p, t):
    b = ax.bar(["Edad (años)", "Tarifa"], [e.mean(), t.mean()], color=["#4C78A8", "#F58518"])
    ax.bar_label(b, fmt="%.2f")
    ax.set_title("Promedios generales")
    return f"edad {e.mean():.2f} | tarifa {t.mean():.2f}"


def est_prom_edad(ax, e, p, t):
    ax.hist(e, bins=15, color="#4C78A8", edgecolor="white")
    ax.axvline(e.mean(), color="red", linestyle="--", label=f"Promedio {e.mean():.2f}")
    ax.set_title("Distribucion de edad")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Pasajeros")
    ax.legend()
    return f"promedio {e.mean():.2f}, mediana {np.median(e):.1f}, desv. {e.std():.2f}"