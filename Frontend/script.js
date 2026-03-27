
const area = document.getElementById("area");
const calidad = document.getElementById("calidad");

area.oninput = () => {
    document.getElementById("area_val").innerText = area.value;
};

calidad.oninput = () => {
    document.getElementById("calidad_val").innerText = calidad.value;
};

let chart = new Chart(document.getElementById("grafica"), {
    type: "bar",
    data: {
        labels: ["-20%", "-10%", "Base", "+10%", "+20%"],
        datasets: [{
            label: "Precio estimado",
            data: [0, 0, 0, 0, 0]
        }]
    },
    options: {
        responsive: true
    }
});


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

            let precio = data.precio;

            document.getElementById("resultado").innerText =
                " Precio estimado: $" + precio;

            chart.data.datasets[0].data = [
                precio * 0.8,
                precio * 0.9,
                precio,
                precio * 1.1,
                precio * 1.2
            ];

            chart.update();
        }

    })
    .catch(err => {
        console.error(err);
        document.getElementById("resultado").innerText =
            "Error de conexión con el backend";
    });
}