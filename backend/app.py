from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predecir_precio

app = Flask(__name__)
CORS(app)

@app.route("/predecir", methods=["POST"])
def predecir_api():

    datos = request.json

    try:
        # 🔥 CONVERSIÓN DE TIPOS (CLAVE)
        calidad = int(datos["calidad"])
        area = int(datos["area"])
        habitaciones = int(datos["habitaciones"])
        banos = int(datos["banos"])
        garaje = int(datos["garaje"])
        anio = int(datos["anio"])

        precio = predecir_precio(
            calidad,
            area,
            habitaciones,
            banos,
            garaje,
            anio
        )

        return jsonify({"precio": precio})

    except KeyError as e:
        return jsonify({"error": f"Falta el dato: {str(e)}"}), 400

    except ValueError:
        return jsonify({"error": "Datos inválidos: asegúrate de enviar números"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

