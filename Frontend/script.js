function predecir() {

    document.getElementById("resultado").innerText = "Calculando... ⏳";

    fetch("http://127.0.0.1:5000/predecir", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            calidad: parseInt(calidad.value),
            area: parseInt(area.value),
            habitaciones: parseInt(document.getElementById("habitaciones").value),
            banos: parseInt(document.getElementById("banos").value),
            garaje: 1
        })
    })
    .then(res => res.json())
    .then(data => {

        if (data.error) {
            document.getElementById("resultado").innerText =
                "Error: " + data.error;
        } else {
            document.getElementById("resultado").innerText =
                "💰 Precio estimado: $" + data.precio;
        }

    })
    .catch(err => {
        document.getElementById("resultado").innerText =
            "Error de conexión con el servidor";
    });
}