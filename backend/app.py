from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predecir_precio

app = Flask(__name__)
CORS(app)

@app.route("/predecir", methods=["POST"])
def predecir():

    datos = request.json

    precio = predecir_precio(
        datos["calidad"],
        datos["area"],
        datos["habitaciones"],
        datos["banos"],
        datos["garaje"]
    )

    return jsonify({"precio": precio})

@app.route("/predecir", methods=["POST"])
def predecir():

    datos = request.json

    try:
        calidad = int(datos["calidad"])
        area = int(datos["area"])
        habitaciones = int(datos["habitaciones"])
        banos = int(datos["banos"])
        garaje = int(datos["garaje"])

        precio = predecir_precio(calidad, area, habitaciones, banos, garaje)

        return jsonify({"precio": precio})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
    app.run(debug=True)
    

