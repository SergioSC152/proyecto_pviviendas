import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# =========================
# CARGAR DATASET
# =========================

df = pd.read_csv("../data/dataset_mazatlan.csv")

print(df.head())

# =========================
# FEATURE ENGINEERING
# =========================

df["edad"] = 2026 - df["anio"]


df["habitaciones_por_bano"] = (
    df["habitaciones"] / (df["banos"] + 1)
)

df["area_por_habitacion"] = (
    df["area"] / df["habitaciones"]
)

# =========================
# LABEL ENCODERS
# =========================

encoder_calidad = LabelEncoder()
encoder_zona = LabelEncoder()
encoder_tipo = LabelEncoder()

df["calidad"] = encoder_calidad.fit_transform(df["calidad"])
df["zona"] = encoder_zona.fit_transform(df["zona"])
df["tipo"] = encoder_tipo.fit_transform(df["tipo"])

# =========================
# VARIABLES X / Y
# =========================

X = df.drop("precio", axis=1)

y = df["precio"]

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# MODELO
# =========================

modelo = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42
)

# =========================
# ENTRENAR
# =========================

modelo.fit(X_train, y_train)

# =========================
# PREDICCIONES
# =========================

predicciones = modelo.predict(X_test)

# =========================
# MÉTRICAS
# =========================

mae = mean_absolute_error(y_test, predicciones)

r2 = r2_score(y_test, predicciones)

print("\n========================")
print("RESULTADOS DEL MODELO")
print("========================")

print(f"MAE: {mae:,.2f}")

print(f"R2 Score: {r2:.4f}")

# =========================
# IMPORTANCIA VARIABLES
# =========================

importancias = pd.DataFrame({
    "Variable": X.columns,
    "Importancia": modelo.feature_importances_
})

importancias = importancias.sort_values(
    by="Importancia",
    ascending=False
)

print("\n========================")
print("IMPORTANCIA VARIABLES")
print("========================")

print(importancias)

# =========================
# GUARDAR MODELO
# =========================

joblib.dump(modelo, "../backend/modelo.pkl")

# =========================
# GUARDAR ENCODERS
# =========================

joblib.dump(encoder_calidad, "../backend/encoder_calidad.pkl")
joblib.dump(encoder_zona, "../backend/encoder_zona.pkl")
joblib.dump(encoder_tipo, "../backend/encoder_tipo.pkl")

print("\n✅ Modelo guardado correctamente")