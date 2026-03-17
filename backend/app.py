from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predecir_precio

app = Flask(__name__)

# 🔥 CORS BIEN CONFIGURADO
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json()

    precio = predecir_precio(
        datos["calidad"],
        datos["area"],
        datos["habitaciones"],
        datos["banos"],
        datos["garaje"]
    )

    return jsonify({"precio": precio})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    