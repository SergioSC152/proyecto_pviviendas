import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def entrenar_y_guardar_modelo():
    data = pd.read_csv("data/train.csv")

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

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    with open("models/modelo_regresion.pkl", "wb") as archivo:
        pickle.dump(modelo, archivo)

    print("Modelo entrenado y guardado correctamente.")

def cargar_modelo():
    with open("models/modelo_regresion.pkl", "rb") as archivo:
        modelo = pickle.load(archivo)
    return modelo

def predecir_precio(calidad, area, habitaciones, banos, garaje):
    modelo = cargar_modelo()
    datos = [[calidad, area, habitaciones, banos, garaje]]
    prediccion = modelo.predict(datos)
    return int(prediccion[0])