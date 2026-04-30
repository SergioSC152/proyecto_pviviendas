import streamlit as st
import requests

# CONFIG
st.set_page_config(
    page_title="SMART HOME PRICE",
    page_icon="logo2.png",
    layout="wide"
)

# --- HEADER ---
st.markdown("""
<div style='
    display:flex;
    align-items:center;
    justify-content:center;
    gap:20px;
    padding: 20px;
    border-radius:20px;
    background: linear-gradient(135deg, #6366F1, #22C55E);
    color:white;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
'>
    <img src="data:image/png;base64,{}" width="80">wg
    <div>
        <h1 style='margin:0;'>SMART HOME PRICE</h1>
        <p style='margin:0;'>Predicción inteligente de precios con IA</p>
    </div>
</div>
""".format(
    __import__("base64").b64encode(open("logo.png", "rb").read()).decode()
), unsafe_allow_html=True)

st.info("💡 Ingresa las características del inmueble y obtén una estimación basada en Machine Learning.")

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.image("logo2.png", width=120)
    st.markdown("## 🏠 SMART HOME")

    st.header("⚙️ Configura tu vivienda")

    # 🔥 SIN + -
    area = int(st.text_input("📐 Área (m²)", "120"))

    # ✅ CON + -
    cuartos = st.number_input("🛏️ Habitaciones", min_value=1, max_value=20, value=3)

    banos = st.number_input("🚿 Baños", min_value=1, max_value=10, value=2)

    # ✅ NUEVO (CON + -)
    garaje = st.number_input("🚗 Garajes", min_value=0, max_value=10, value=1)

    calidad = st.selectbox("⭐ Calidad", ["Mala", "Regular", "Buena", "Excelente", "Lujo"])

    # 🔥 SIN + -
    anio = int(st.text_input("Año de construcción", "2005"))

    ubicacion = st.selectbox("📍 Ubicación", ["Centro", "Norte", "Sur", "Suburbio"])

    st.divider()

    predecir_btn = st.button("🔮 Predecir Precio", use_container_width=True)

# --- ESTADO ---
if 'precio' not in st.session_state:
    st.session_state.precio = 0

st.divider()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Predicción", "📈 Visualización", "🧠 Modelo"])

# ===================== TAB 1 =====================
with tab1:
    st.subheader("🗺️ Ubicación del inmueble")

    import pandas as pd

    data_mapa = pd.DataFrame({
        'lat': [23.2494],
        'lon': [-106.4111]
    })

    st.map(data_mapa)
    st.caption("📍 Mazatlán, Sinaloa")

    st.divider()

    st.subheader("💰 Resultado de la predicción")

    if predecir_btn:
        try:
            mapa_calidad = {
                "Mala": 1,
                "Regular": 2,
                "Buena": 3,
                "Excelente": 4,
                "Lujo": 5
            }

            data = {
                "calidad": mapa_calidad[calidad],
                "area": area,
                "habitaciones": int(cuartos),
                "banos": int(banos),
                "garaje": int(garaje),
                "anio": anio
            }

            response = requests.post("http://127.0.0.1:5000/predecir", json=data)

            if response.status_code == 200:
                resultado = response.json()

                precio_base = resultado["precio"]

                factores_ubicacion = {
                    "Centro": 1.25,
                    "Norte": 1.15,
                    "Sur": 0.95,
                    "Suburbio": 0.85
                }

                factor = factores_ubicacion[ubicacion]
                precio = precio_base * factor

                st.session_state.precio = precio

                # 💱 Conversión
                TASA_USD_MXN = 17.0
                precio_mxn = precio * TASA_USD_MXN

                st.balloons()

                st.success(f"""
                ## 💰 ${precio:,.2f} USD
                ## 🇲🇽 ${precio_mxn:,.2f} MXN
                ### 📍 Ubicación: {ubicacion}
                """)

                st.info(f"📍 Factor de ubicación aplicado: x{factor}")
                st.info("💱 Conversión aproximada basada en tasa USD → MXN")
                st.caption("La conversión es referencial.")
                st.info("📌 Estimación basada en Machine Learning.")

                st.progress(92)

            else:
                st.error("❌ Error en el servidor")

        except Exception as e:
            st.error(f"❌ Error en los datos: {e}")

# ===================== TAB 2 =====================
with tab2:
    st.subheader("📊 Distribución de precios")

    st.bar_chart([120000, 150000, 170000, 140000, 200000])

    st.write("📈 Datos simulados")

# ===================== TAB 3 =====================
with tab3:
    st.subheader("🧠 Información del modelo")

    st.code("""
Modelo: Random Forest
Variables:
- Área
- Habitaciones
- Baños
- Garajes
- Calidad
- Año de construcción
""")

    with st.expander("🔍 ¿Cómo funciona?"):
        st.write("El modelo analiza datos históricos.")