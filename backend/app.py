from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predecir_precio

app = Flask(__name__)
CORS(app)

@app.route("/predecir", methods=["POST"])
def predecir_api():   

    datos = request.json

    precio = predecir_precio(
     datos["calidad"],
     datos["area"],
     datos["habitaciones"],
     datos["banos"],
     datos["garaje"],
     datos["anio"]
    )
    

    return jsonify({"precio": precio})


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
    

