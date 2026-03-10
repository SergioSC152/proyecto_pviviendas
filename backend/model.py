import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def entrenar_y_guardar_modelo():

    data = pd.read_csv("data/train.csv")

    print("Número de filas del dataset:", data.shape[0])
    print("Número de columnas del dataset:", data.shape[1])

    X = data[[
        "OverallQual",
        "GrLivArea",
        "BedroomAbvGr",
        "FullBath",
        "GarageCars"
    ]]
    print("Variables utilizadas para el modelo:")
    print(X.columns)
    y = data["SalePrice"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)

    y_pred_lr = modelo_lr.predict(X_test)

    r2_lr = r2_score(y_test, y_pred_lr)
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))

    print("=== Evaluación Regresión Lineal ===")
    print("R2:", r2_lr)
    print("MAE:", mae_lr)
    print("RMSE:", rmse_lr)

    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    y_pred_rf = modelo_rf.predict(X_test)

    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

    print("\n=== Evaluación Random Forest ===")
    print("R2:", r2_rf)
    print("MAE:", mae_rf)
    print("RMSE:", rmse_rf)

    with open("models/evaluacion.txt", "w") as f:

        f.write("=== Evaluación Regresión Lineal ===\n")
        f.write(f"R2: {r2_lr}\n")
        f.write(f"MAE: {mae_lr}\n")
        f.write(f"RMSE: {rmse_lr}\n\n")

        f.write("=== Evaluación Random Forest ===\n")
        f.write(f"R2: {r2_rf}\n")
        f.write(f"MAE: {mae_rf}\n")
        f.write(f"RMSE: {rmse_rf}\n")

    if r2_rf > r2_lr:
        mejor_modelo = modelo_rf
        print("\nSe seleccionó Random Forest como mejor modelo")
    else:
        mejor_modelo = modelo_lr
        print("\nSe seleccionó Regresión Lineal como mejor modelo")

    with open("models/modelo_regresion.pkl", "wb") as archivo:
        pickle.dump(mejor_modelo, archivo)

    print("\nModelo guardado correctamente.")

def cargar_modelo():

    with open("models/modelo_regresion.pkl", "rb") as archivo:
        modelo = pickle.load(archivo)

    return modelo

def predecir_precio(calidad, area, habitaciones, banos, garaje):

    modelo = cargar_modelo()

    datos = [[calidad, area, habitaciones, banos, garaje]]

    prediccion = modelo.predict(datos)

    print("Predicción generada correctamente.")

    return int(prediccion[0])
