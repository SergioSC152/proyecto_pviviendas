import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


def entrenar_y_guardar_modelo():

    data = pd.read_csv("../data/train.csv")

    print("Número de filas del dataset:", data.shape[0])
    print("Número de columnas del dataset:", data.shape[1])

    # Variables del modelo (se mantiene igual)
    X = data[[
        "OverallQual",
        "GrLivArea",
        "BedroomAbvGr",
        "FullBath",
        "GarageCars",
        "YearBuilt"
    ]]

    print("Variables utilizadas para el modelo:")
    print(X.columns)

    y = data["SalePrice"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Modelos
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)

    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    # Selección del mejor modelo
    if modelo_rf.score(X_test, y_test) > modelo_lr.score(X_test, y_test):
        mejor_modelo = modelo_rf
        print("Se eligió Random Forest")
    else:
        mejor_modelo = modelo_lr
        print("Se eligió Regresión Lineal")

    # Guardar modelo
    with open("../models/modelo_regresion.pkl", "wb") as archivo:
        pickle.dump(mejor_modelo, archivo)

    print("Modelo guardado correctamente.")


def cargar_modelo():
    with open("../models/modelo_regresion.pkl", "rb") as archivo:
        modelo = pickle.load(archivo)
    return modelo


# 🔥 NUEVA FUNCIÓN PARA AJUSTAR CALIDAD (CLAVE)
def ajustar_por_calidad(precio, calidad):

    factores = {
        1: 0.95,   # Mala
        2: 1.0,    # Regular
        3: 1.05,   # Buena
        4: 1.08,   # Excelente (ya no exagera)
        5: 1.12    # Lujo (controlado)
    }

    return precio * factores.get(calidad, 1)


# FUNCIÓN DE PREDICCIÓN ACTUALIZADA
def predecir_precio(calidad, area, habitaciones, banos, garaje, anio):

    modelo = cargar_modelo()

    datos = [[calidad, area, habitaciones, banos, garaje, anio]]
    prediccion = modelo.predict(datos)

    precio_base = prediccion[0]

    # 🔥 Ajuste controlado de calidad
    precio_ajustado = ajustar_por_calidad(precio_base, calidad)

    print("Predicción generada correctamente.")

    return int(precio_ajustado)


# Ejecutar entrenamiento si se corre directamente
if __name__ == "__main__":
    entrenar_y_guardar_modelo()