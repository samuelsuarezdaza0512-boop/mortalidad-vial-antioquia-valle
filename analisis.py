#!/usr/bin/env python3
"""Regenera las tablas e imágenes del paper desde datos/indicadores_2016_2024.csv."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datos" / "indicadores_2016_2024.csv"
OUT = ROOT / "figuras"
OUT.mkdir(exist_ok=True)
d = pd.read_csv(DATA)

def line_plot(cols, labels, title, ylabel, filename):
    plt.figure(figsize=(10, 5.5))
    for col, label in zip(cols, labels):
        plt.plot(d["anio"], d[col], marker="o", linewidth=2, label=label)
    plt.title(title)
    plt.xlabel("Año")
    plt.ylabel(ylabel)
    plt.xticks(d["anio"])
    plt.grid(alpha=.25)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=180)
    plt.close()

line_plot(
    ["fallecidos_antioquia", "fallecidos_valle"],
    ["Antioquia", "Valle del Cauca"],
    "Fallecidos en siniestros viales por departamento (2016–2024)",
    "Personas fallecidas", "figura1_conteo_fallecidos.png"
)
line_plot(
    ["tasa_mortalidad_antioquia", "tasa_mortalidad_valle"],
    ["Antioquia", "Valle del Cauca"],
    "Tasa de mortalidad vial por cada 100.000 habitantes (2016–2024)",
    "Fallecidos por cada 100.000 habitantes", "figura2_tasa_mortalidad.png"
)

plt.figure(figsize=(11, 6))
for col, label in [
    ("primas_antioquia_miles_millones", "Antioquia – primas"),
    ("siniestros_antioquia_miles_millones", "Antioquia – siniestros pagados"),
    ("primas_valle_miles_millones", "Valle – primas"),
    ("siniestros_valle_miles_millones", "Valle – siniestros pagados"),
]:
    plt.plot(d["anio"], d[col], marker="o", linewidth=2, label=label)
plt.title("Primas emitidas y siniestros pagados en diciembre (2016–2024)")
plt.xlabel("Año")
plt.ylabel("Miles de millones de COP corrientes")
plt.xticks(d["anio"]); plt.grid(alpha=.25); plt.legend(frameon=False, ncol=2)
plt.tight_layout()
plt.savefig(OUT / "figura3_primas_siniestros.png", dpi=180)
plt.close()

plt.figure(figsize=(11, 6))
for col, label in [
    ("tasa_mortalidad_antioquia", "Antioquia – tasa de mortalidad"),
    ("siniestralidad_antioquia", "Antioquia – siniestralidad"),
    ("tasa_mortalidad_valle", "Valle del Cauca – tasa de mortalidad"),
    ("siniestralidad_valle", "Valle del Cauca – siniestralidad"),
]:
    values = d[col]
    plt.plot(d["anio"], values / values.iloc[0] * 100, marker="o", linewidth=2, label=label)
plt.axhline(100, linewidth=1)
plt.title("Comparación de tendencias: índice 2016 = 100")
plt.xlabel("Año"); plt.ylabel("Índice (2016 = 100)")
plt.xticks(d["anio"]); plt.grid(alpha=.25); plt.legend(frameon=False, ncol=2)
plt.tight_layout()
plt.savefig(OUT / "figura4_tendencias_comparadas.png", dpi=180)
plt.close()

for dept, mortality, loss in [
    ("Antioquia", "tasa_mortalidad_antioquia", "siniestralidad_antioquia"),
    ("Valle del Cauca", "tasa_mortalidad_valle", "siniestralidad_valle"),
]:
    corr_levels = d[mortality].corr(d[loss])
    corr_diffs = d[mortality].diff().corr(d[loss].diff())
    same_direction = (
        (d[mortality].diff().dropna().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
         == d[loss].diff().dropna().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))).sum()
    )
    print(f"{dept}: Pearson niveles={corr_levels:.3f}; primeras diferencias={corr_diffs:.3f}; "
          f"mismo sentido={same_direction}/8 cambios")

print(f"Figuras regeneradas en {OUT}")
