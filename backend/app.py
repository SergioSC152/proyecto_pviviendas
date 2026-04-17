from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predecir_precio

app = Flask(__name__)
CORS(app)

@app.route("/predecir", methods=["POST"])
def predecir_api():

    datos = request.json

    try:
        precio = predecir_precio(
            datos["calidad"],
            datos["area"],
            datos["habitaciones"],
            datos["banos"],
            datos["garaje"],
            datos["anio"]  # 🔥 NUEVA VARIABLE
        )

        return jsonify({"precio": precio})

    except KeyError as e:
        return jsonify({"error": f"Falta el dato: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

