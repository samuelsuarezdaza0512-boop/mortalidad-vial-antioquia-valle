# Análisis reproducible (R)
# Revise los nombres y encabezados de hojas de los Excel antes de ejecutar.
# Este script es un punto de entrada documentado; no reemplaza la inspección de las fuentes.
library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)
library(readr)

f_mort <- "datos/Datos_Antioquia_ValleDelCauca.xlsx"
f_extra <- "datos/Datos_Siniestros_Viales_v2.xlsx"

# Inspección de hojas disponible para auditar los insumos:
print(excel_sheets(f_mort))
print(excel_sheets(f_extra))

# La tabla central debe prepararse conservando los valores originales y
# dejando documentada la fuente/URL/fecha de cada serie.
# No imputar valores ausentes ni interpretar diciembre como acumulado anual.
# Una vez consolidada, exportar como datos/tabla_central.csv con columnas:
# departamento, anio, fallecidos, poblacion, tasa_mortalidad.
