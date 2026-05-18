from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import pandas as pd

# =========================
# CARGAR MODELO
# =========================

modelo = joblib.load("modelo.pkl")

encoder_calidad = joblib.load("encoder_calidad.pkl")
encoder_zona = joblib.load("encoder_zona.pkl")
encoder_tipo = joblib.load("encoder_tipo.pkl")

# =========================
# APP FLASK
# =========================

app = Flask(__name__)

CORS(app)

# =========================
# RUTA PREDICCIÓN
# =========================

@app.route("/predecir", methods=["POST"])
def predecir_api():

    try:

        datos = request.json

        # =========================
        # DATOS FRONTEND
        # =========================

        area = int(datos["area"])

        habitaciones = int(datos["habitaciones"])

        banos = int(datos["banos"])

        garaje = int(datos["garaje"])

        anio = int(datos["anio"])

        calidad = datos["calidad"]

        zona = datos["zona"]

        tipo = datos["tipo"]

        # =========================
        # ENCODERS
        # =========================

        calidad_encoded = encoder_calidad.transform([calidad])[0]

        zona_encoded = encoder_zona.transform([zona])[0]

        tipo_encoded = encoder_tipo.transform([tipo])[0]

        # =========================
        # VARIABLES DERIVADAS
        # =========================

        edad = 2026 - anio

        habitaciones_por_bano = habitaciones / banos

        area_por_habitacion = area / habitaciones

        # =========================
        # DATAFRAME
        # =========================

        nuevo = pd.DataFrame([{
        "area": area,
        "habitaciones": habitaciones,
        "banos": banos,
        "garaje": garaje,
        "calidad": calidad_encoded,
        "zona": zona_encoded,
        "tipo": tipo_encoded,
        "anio": anio,
        "edad": edad,
        "habitaciones_por_bano": habitaciones_por_bano,
        "area_por_habitacion": area_por_habitacion
}])
        # =========================
        # PREDICCIÓN IA
        # =========================

        prediccion = modelo.predict(nuevo)[0]

        return jsonify({
            "precio": round(prediccion, 2)
        })

    except Exception as e:

     print("\n================ ERROR BACKEND ================\n")
     print(e)
     print("\n===============================================\n")

     return jsonify({
        "error": str(e)
     }), 500

# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(debug=True)

