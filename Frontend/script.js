const area = document.getElementById("area");
const calidad = document.getElementById("calidad");

area.oninput = () => {
    document.getElementById("area_val").innerText = area.value;
};

calidad.oninput = () => {
    document.getElementById("calidad_val").innerText = calidad.value;
};

// GRAFICA
let chart = new Chart(document.getElementById("grafica"), {
    type: "bar",
    data: {
        labels: ["Base", "Zona", "Tamaño", "Extras", "Final"],
        datasets: [{
            label: "Precio",
            data: [100000, 150000, 140000, 160000, 130000]
        }]
    }
});

// PREDICCIÓN
function predecir() {

    fetch("http://127.0.0.1:5000/predecir",  {
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
    .then(async res => {
        const text = await res.text();

        if (!res.ok) {
            throw new Error("Backend dice: " + text);
        }

        return JSON.parse(text);
    })
    .then(data => {

        document.getElementById("resultado").innerText =
            "Precio estimado: $" + data.precio;

    })
    .catch(err => {
        console.error("ERROR REAL:", err);
        document.getElementById("resultado").innerText =
            err.message;
    });
}

