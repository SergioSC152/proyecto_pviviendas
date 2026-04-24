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
    padding: 20px;
    border-radius: 10px;
}

h1, h2, h3 {
    color: #1f2937;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    color: #0ea5e9;
}
</style>
""", unsafe_allow_html=True)

# ------------------ NAVBAR ------------------
st.markdown('<div class="logo">🏠 SMART HOME</div>', unsafe_allow_html=True)

# ------------------ CONTROL DE PASOS ------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "precio" not in st.session_state:
    st.session_state.precio = 0

# ------------------ HOME ------------------
if st.session_state.step == 0:
    st.title("Bienvenido a SMART HOME")
    st.write("Sistema de predicción de precios de viviendas con IA")

    if st.button("📊 Generar Reporte"):
        st.session_state.step = 1

# ------------------ PASO 1 ------------------
elif st.session_state.step == 1:

    st.title("📍 Ubicación del inmueble")

    col1, col2 = st.columns(2)

    with col1:
        direccion = st.text_input("Dirección")
        calle = st.text_input("Calle")
        numero = st.text_input("Número exterior")
        cp = st.text_input("Código postal")

    with col2:
        st.info("🗺️ Mapa interactivo próximamente")

    if st.button("➡️ Siguiente"):
        st.session_state.step = 2

# ------------------ PASO 2 ------------------
elif st.session_state.step == 2:

    st.title("🏠 Características del inmueble")

    col1, col2 = st.columns(2)

    with col1:
        area = st.slider("Área (m²)", 50, 500, 120)
        habitaciones = st.slider("Habitaciones", 1, 5, 3)
        banos = st.slider("Baños", 1, 3, 2)

    with col2:
        garaje = st.slider("Garaje", 0, 3, 1)
        anio = st.slider("Año de construcción", 1950, 2023, 2005)
        calidad = st.selectbox("Calidad", ["Mala", "Regular", "Buena", "Excelente", "Lujo"])
        ubicacion = st.selectbox("📍 Zona en Mazatlán", ["Centro", "Norte", "Sur", "Suburbio"])

    if st.button("🔮 Predecir"):
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
                resultado = response.json()

                # 🔥 PRECIO BASE DEL MODELO
                precio_base = resultado["precio"]

                # 🔥 FACTORES POR ZONA (AQUÍ ESTÁ LO IMPORTANTE)
                factores = {
                    "Centro": 1.25,
                    "Norte": 1.15,
                    "Sur": 0.95,
                    "Suburbio": 0.85
                }

                factor = factores[ubicacion]

                # 🔥 PRECIO AJUSTADO
                precio = precio_base * factor

                # Guardar resultado
                st.session_state.precio = precio
                st.session_state.factor = factor
                st.session_state.zona = ubicacion

                st.session_state.step = 3

            else:
                st.error("❌ Error en el backend")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ------------------ PASO 3 ------------------
elif st.session_state.step == 3:

    st.title("💰 Resultado de la predicción")

    precio = st.session_state.precio
    factor = st.session_state.factor
    zona = st.session_state.zona

    # 💱 Conversión
    TASA = 17.0
    precio_mxn = precio * TASA

    st.success("Predicción completada")

    st.markdown(f"## 💵 ${precio:,.2f} USD")
    st.markdown(f"## 🇲🇽 ${precio_mxn:,.2f} MXN")

    # 🔥 INFO PRO
    st.info(f"📍 Zona: {zona} | Factor aplicado: x{factor}")

    st.caption("La predicción fue ajustada según el mercado local de Mazatlán")

    if st.button("🔄 Nuevo cálculo"):
        st.session_state.step = 0