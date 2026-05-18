import pandas as pd
import random

# =========================
# CONFIGURACIÓN ZONAS
# =========================

zonas = {
    "Marina Mazatlan": 58000,
    "Zona Dorada": 62000,
    "Cerritos": 32000,
    "Centro": 22000,
    "Pradera Dorada": 16000,
    "Villas del Rey": 14000
}

calidades = {
    "Mala": 0.80,
    "Regular": 0.92,
    "Buena": 1.00,
    "Excelente": 1.12,
    "Lujo": 1.25
}

tipos = ["Casa", "Departamento"]

dataset = []

# =========================
# GENERAR 3000 PROPIEDADES
# =========================

for i in range(3000):

    zona = random.choice(list(zonas.keys()))

    tipo = random.choice(tipos)

    # =========================
    # ÁREA SEGÚN TIPO
    # =========================

    if tipo == "Casa":
        area = random.randint(60, 450)
    else:
        area = random.randint(45, 300)

    # =========================
    # HABITACIONES SEGÚN ÁREA
    # =========================

    if area <= 80:
     habitaciones = random.randint(1, 2)

    elif area <= 150:
     habitaciones = random.randint(2, 3)

    elif area <= 250:
     habitaciones = random.randint(3, 4)

    else:
     habitaciones = random.randint(4, 6)

    # =========================
    # BAÑOS COHERENTES
    # =========================

    if habitaciones <= 2:
     banos = random.randint(1, 2)

    elif habitaciones <= 4:
     banos = random.randint(2, 4)

    else:
     banos = random.randint(3, 5)
 
    # =========================
    # GARAJE COHERENTE
    # =========================

    if tipo == "Departamento":
     garaje = random.randint(0, 2)

    else:

     if area <= 120:
        garaje = random.randint(0, 1)

     elif area <= 250:
        garaje = random.randint(1, 2)

     else:
        garaje = random.randint(2, 4)

    # =========================
    # CALIDAD
    # =========================

    calidad = random.choice(list(calidades.keys()))

    # =========================
    # AÑO
    # =========================

    anio = random.randint(1990, 2026)

    # =========================
    # PRECIO BASE
    # =========================

    precio_m2 = zonas[zona]

    precio = area * precio_m2

    # =========================
    # AJUSTE CALIDAD
    # =========================

    precio *= calidades[calidad]

    # =========================
    # AJUSTE TIPO
    # =========================

    if tipo == "Departamento":

       if zona in ["Marina Mazatlan", "Zona Dorada"]:
          precio *= 1.18
       else:
          precio *= 1.05

    # =========================
    # AJUSTE HABITACIONES
    # =========================

    precio += habitaciones * random.randint(120000, 280000)

    # =========================
    # AJUSTE BAÑOS
    # =========================

    precio += banos * random.randint(180000, 450000)

    # =========================
    # AJUSTE GARAJE
    # =========================

    precio += garaje * random.randint(80000, 250000)

    # =========================
    # AJUSTE ANTIGÜEDAD
    # =========================

    edad = 2026 - anio

    if edad <= 3:
        precio *= 1.18

    elif edad <= 10:
        precio *= 1.08

    elif edad >= 25:
        precio *= 0.82

    # =========================
    # RUIDO ALEATORIO
    # =========================

    ruido = random.uniform(0.90, 1.10)

    precio *= ruido

    # =========================
    # GUARDAR FILA
    # =========================

    dataset.append([
        area,
        habitaciones,
        banos,
        garaje,
        calidad,
        zona,
        tipo,
        anio,
        round(precio)
    ])

# =========================
# CREAR DATAFRAME
# =========================

df = pd.DataFrame(dataset, columns=[
    "area",
    "habitaciones",
    "banos",
    "garaje",
    "calidad",
    "zona",
    "tipo",
    "anio",
    "precio"
])

# =========================
# GUARDAR CSV
# =========================

df.to_csv("../data/dataset_mazatlan.csv", index=False)

print("✅ Dataset generado correctamente")
print(df.head())