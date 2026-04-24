import streamlit as st
import requests

st.set_page_config(page_title="SMART HOME", layout="wide")

# ------------------ ESTILOS ------------------
st.markdown("""
<style>
html, body {
    background-color: #f5f7fa;
}

.block-container {
    background-color: white;
    padding: 30px;
    border-radius: 12px;
}

h1, h2 {
    color: #1f2937;
}

.boton {
    background-color: #0ea5e9;
    color: white;
    padding: 12px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ ESTADO ------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "precio" not in st.session_state:
    st.session_state.precio = 0

# ------------------ PANTALLA PRINCIPAL ------------------
if st.session_state.step == 0:

    st.title("🏠 SMART HOME PRICE")

    col1, col2 = st.columns(2)

    # -------- IZQUIERDA: CARACTERÍSTICAS --------
    with col1:
        st.subheader("Características")

        area = st.slider("Área (m²)", 50, 500, 120)
        habitaciones = st.slider("Habitaciones", 1, 5, 3)
        banos = st.slider("Baños", 1, 3, 2)
        garaje = st.slider("Garaje", 0, 3, 1)
        anio = st.slider("Año de construcción", 1950, 2023, 2005)

        calidad = st.selectbox(
            "Calidad",
            ["Mala", "Regular", "Buena", "Excelente", "Lujo"]
        )

        st.subheader("Selecciona zona")

        zonas = [
            ["Noroeste", "Norte", "Noreste"],
            ["Oeste", "Centro", "Este"],
            ["Suroeste", "Sur", "Sureste"]
        ]

        for fila in zonas:
            cols = st.columns(3)
            for i, zona in enumerate(fila):
                if cols[i].button(zona):
                    st.session_state.zona = zona

        if "zona" in st.session_state:
            st.success(f"Zona: {st.session_state.zona}")

    # -------- DERECHA: MAPA --------
    with col2:
        st.subheader("Mapa de Mazatlán")

        st.markdown("""
        <div style="
            height: 400px;
            background-color: #e5e7eb;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: #6b7280;
        ">
            🗺️ Aquí irá el mapa de Mazatlán
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # -------- BOTÓN CONTINUAR --------
    if st.button("🚀 Continuar y predecir", use_container_width=True):

        if "zona" not in st.session_state:
            st.error("⚠️ Debes seleccionar una zona")
            st.stop()

        try:
            mapa_calidad = {
                "Mala": 2,
                "Regular": 4,
                "Buena": 6,
                "Excelente": 8,
                "Lujo": 10
            }

            data = {
                "calidad": mapa_calidad[calidad],
                "area": area,
                "habitaciones": habitaciones,
                "banos": banos,
                "garaje": garaje,
                "anio": anio
            }

            response = requests.post("http://127.0.0.1:5000/predecir", json=data)

            if response.status_code == 200:
                precio_base = response.json()["precio"]

                factores = {
                    "Centro": 1.30,
                    "Norte": 1.15,
                    "Sur": 0.90,
                    "Este": 1.05,
                    "Oeste": 1.10,
                    "Noreste": 1.20,
                    "Noroeste": 1.18,
                    "Sureste": 0.95,
                    "Suroeste": 0.85
                }

                zona = st.session_state.zona
                factor = factores[zona]

                precio = precio_base * factor

                st.session_state.precio = precio
                st.session_state.zona = zona
                st.session_state.factor = factor

                st.session_state.step = 1

            else:
                st.error("❌ Error en el backend")

        except Exception as e:
            st.error(f"❌ Error: {e}")


# ------------------ RESULTADO ------------------
elif st.session_state.step == 1:

    st.title("💰 Resultado de la predicción")

    precio = st.session_state.precio
    zona = st.session_state.zona
    factor = st.session_state.factor

    TASA = 17.0
    precio_mxn = precio * TASA

    st.success("Predicción completada")

    st.markdown(f"## 💵 ${precio:,.2f} USD")
    st.markdown(f"## 🇲🇽 ${precio_mxn:,.2f} MXN")

    st.info(f"📍 Zona: {zona} | Ajuste aplicado: x{factor}")

    if st.button("🔄 Nuevo cálculo"):
        st.session_state.step = 0
        