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

def est_prom_tarifa(ax, e, p, t):
    ax.hist(t, bins=25, color="#F58518", edgecolor="white")
    ax.axvline(t.mean(), color="red", linestyle="--", label=f"Promedio {t.mean():.2f}")
    ax.set_title("Distribucion de tarifa\n(sustituye dias de estancia)")
    ax.set_xlabel("Tarifa")
    ax.set_ylabel("Pasajeros")
    ax.legend()
    return f"promedio {t.mean():.2f}, mediana {np.median(t):.2f}, desv. {t.std():.2f}"

def est_rango_edad_tarifa(ax, e, p, t):
    cortes = [13, 18, 30, 45, 60]
    etiquetas = ["0-12", "13-17", "18-29", "30-44", "45-59", "60+"]
    idx = np.digitize(e, cortes)  # 0..5
    prom = [t[idx == i].mean() if np.any(idx == i) else 0 for i in range(len(etiquetas))]
    b = ax.bar(etiquetas, prom, color="#B279A2")
    ax.bar_label(b, fmt="%.2f")
    ax.set_title("Rango de edad vs tarifa promedio\n(sustituye dias de estancia)")
    ax.set_xlabel("Rango de edad")
    ax.set_ylabel("Tarifa promedio")
    return " | ".join(f"{l}: {v:.2f}" for l, v in zip(etiquetas, prom))

# (texto de la casilla, funcion)
ESTADISTICOS = [
    ("Promedios generales", est_promedios),
    ("Promedio de edad", est_prom_edad),
    ("Promedio de tarifa", est_prom_tarifa),
    ("Viajeros vs puerto", est_viajeros_puerto),
    ("Rango de edad vs tarifa", est_rango_edad_tarifa),
]


def dibujar(elegidos, edades, puertos, tarifas):
    """Dibuja los estadisticos elegidos como subplots de una sola figura.

        elegidos: lista de (nombre, funcion).
        Devuelve (imagen_base64, texto_resumen, columnas).
        """
    n = len(elegidos)
    cols = 1 if n == 1 else 2
    filas = math.ceil(n / cols)
    fig, axes = plt.subplots(filas, cols, figsize=(6.5 * cols, 4.3 * filas), squeeze=False)
    axes = axes.flatten()

    lineas = []
    for ax, (nombre, f) in zip(axes, elegidos):
        lineas.append(f"{nombre}: {f(ax, edades, puertos, tarifas)}")
    for ax in axes[n:]:
        ax.axis("off")  # oculta subplots vacios
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode(), "\n".join(lineas), cols
