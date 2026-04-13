import pandas as pd
import numpy as np
import os
import pickle

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

BASE_DIR = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(BASE_DIR, "../data/train.csv"))
model_path = os.path.abspath(os.path.join(BASE_DIR, "../models/modelo_regresion.pkl"))

data = pd.read_csv(data_path)

X = data[[
    "OverallQual",
    "GrLivArea",
    "BedroomAbvGr",
    "FullBath",
    "GarageCars"
]]
y = data["SalePrice"]

with open(model_path, "rb") as f:
    modelo = pickle.load(f)

y_pred = modelo.predict(X)

r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

print(" EVALUACIÓN DEL MODELO")
print("----------------------------")
print("R2:", r2)
print("MAE:", mae)
print("RMSE:", rmse)