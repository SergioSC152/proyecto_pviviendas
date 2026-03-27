import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def entrenar_y_guardar_modelo():

    data = pd.read_csv("../data/train.csv")

    X = data[[
        "OverallQual",
        "GrLivArea",
        "BedroomAbvGr",
        "FullBath",
        "GarageCars"
    ]]
    y = data["SalePrice"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

   
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)

    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    
    if modelo_rf.score(X_test, y_test) > modelo_lr.score(X_test, y_test):
        mejor_modelo = modelo_rf
        print("Se eligió Random Forest")
    else:
        mejor_modelo = modelo_lr
        print("Se eligió Regresión Lineal")

    
    with open("../models/modelo_regresion.pkl", "wb") as archivo:
        pickle.dump(mejor_modelo, archivo)

    print("Modelo guardado correctamente.")


def cargar_modelo():
    with open("../models/modelo_regresion.pkl", "rb") as archivo:
        modelo = pickle.load(archivo)
    return modelo


def predecir_precio(calidad, area, habitaciones, banos, garaje):

    modelo = cargar_modelo()

    datos = [[calidad, area, habitaciones, banos, garaje]]
    prediccion = modelo.predict(datos)

    return int(prediccion[0])



if __name__ == "__main__":
    entrenar_y_guardar_modelo()