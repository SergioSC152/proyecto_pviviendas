import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def entrenar_y_guardar_modelo():

    data = pd.read_csv("../data/train.csv")

    print("Número de filas del dataset:", data.shape[0])
    print("Número de columnas del dataset:", data.shape[1])

    # Variables (se agregó YearBuilt)
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

    # Modelo Regresión Lineal
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)
    y_pred_lr = modelo_lr.predict(X_test)

    r2_lr = r2_score(y_test, y_pred_lr)
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))

    print("\n=== Regresión Lineal ===")
    print("R2:", r2_lr)
    print("MAE:", mae_lr)
    print("RMSE:", rmse_lr)

    # Modelo Random Forest
    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)
    y_pred_rf = modelo_rf.predict(X_test)

    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

    print("\n=== Random Forest ===")
    print("R2:", r2_rf)
    print("MAE:", mae_rf)
    print("RMSE:", rmse_rf)

    # Guardar métricas en archivo
    with open("../models/evaluacion.txt", "w") as f:
        f.write("=== Regresión Lineal ===\n")
        f.write(f"R2: {r2_lr}\nMAE: {mae_lr}\nRMSE: {rmse_lr}\n\n")

        f.write("=== Random Forest ===\n")
        f.write(f"R2: {r2_rf}\nMAE: {mae_rf}\nRMSE: {rmse_rf}\n")

    # Selección del mejor modelo
    if r2_rf > r2_lr:
        mejor_modelo = modelo_rf
        print("\nSe eligió Random Forest")
    else:
        mejor_modelo = modelo_lr
        print("\nSe eligió Regresión Lineal")

    # Guardar modelo
    with open("../models/modelo_regresion.pkl", "wb") as archivo:
        pickle.dump(mejor_modelo, archivo)

    print("Modelo guardado correctamente.")


def cargar_modelo():
    with open("../models/modelo_regresion.pkl", "rb") as archivo:
        modelo = pickle.load(archivo)
    return modelo


def predecir_precio(calidad, area, habitaciones, banos, garaje, anio):

    modelo = cargar_modelo()

    datos = [[calidad, area, habitaciones, banos, garaje, anio]]

    print("Datos enviados al modelo:", datos)

    prediccion = modelo.predict(datos)

    print("Predicción generada correctamente.")

    return int(prediccion[0])


if _name_ == "_main_":
    entrenar_y_guardar_modelo()
