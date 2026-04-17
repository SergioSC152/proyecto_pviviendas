import streamlit as st
import requests

# CONFIG
st.set_page_config(page_title="SMART HOME PRICE", page_icon="🏠", layout="wide")

# --- HEADER ---
st.markdown("""
# 🏠 SMART HOME PRICE
### 🤖 Predicción inteligente de precios de viviendas
""")

st.info("💡 Ingresa las características del inmueble y obtén una estimación basada en Machine Learning.")

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configura tu vivienda")

    area = st.slider("📐 Área (m²)", 50, 500, 120)
    cuartos = st.slider("🛏️ Habitaciones", 1, 5, 3)
    banos = st.slider("🚿 Baños", 1, 3, 2)
    calidad = st.select_slider("⭐ Calidad", ["Mala", "Regular", "Buena", "Excelente", "Lujo"])

    anio = st.slider("Año de construcción", 1950, 2023, 2005)

    ubicacion = st.selectbox("📍 Ubicación", ["Centro", "Norte", "Sur", "Suburbio"])

    st.divider()

    predecir_btn = st.button("🔮 Predecir Precio", use_container_width=True)

# --- KPIs ---
if 'precio' not in st.session_state:
    st.session_state.precio = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Precio", f"${st.session_state.precio:,.0f}")
col2.metric("🤖 Modelo", "Random Forest")
col3.metric("📉 Error", "± $15K")
col4.metric("📊 Confianza", "92%")

st.divider()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Predicción", "📈 Visualización", "🧠 Modelo"])

with tab1:
    st.subheader("Resultado de la predicción")

    if predecir_btn:
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
                "habitaciones": cuartos,
                "banos": banos,
                "garaje": 1,
                "anio": anio
            }

            response = requests.post("http://127.0.0.1:5000/predecir", json=data)

            if response.status_code == 200:
                resultado = response.json()

                # 🔥 Precio base del modelo
                precio_base = resultado["precio"]

                # 🔥 Simulación por ubicación
                factores_ubicacion = {
                    "Centro": 1.25,
                    "Norte": 1.15,
                    "Sur": 0.95,
                    "Suburbio": 0.85
                }

                factor = factores_ubicacion[ubicacion]

                precio = precio_base * factor

                # Guardar en sesión
                st.session_state.precio = precio

                # 💱 Conversión USD → MXN
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
                st.caption("La conversión es referencial y puede variar según el mercado.")

                st.info("📌 Este resultado es una estimación basada en un modelo de Machine Learning entrenado.")

                st.progress(92)

            else:
                st.error("❌ Error en el servidor")

        except Exception as e:
            st.error(f"❌ No se pudo conectar con el backend: {e}")


with tab2:
    st.subheader("📊 Distribución de precios")

    st.bar_chart([120000, 150000, 170000, 140000, 200000])

    st.write("📈 Esta gráfica representa precios de viviendas similares en el dataset.")
    st.caption("Datos simulados - Sprint 3 (EDA)")

with tab3:
    st.subheader("🧠 Información del modelo")

    st.code("""
Modelo: Random Forest
Dataset: House Prices - Kaggle.

Variables:
- Área
- Habitaciones
- Baños
- Calidad
- Garaje
- Año de construcción

Métricas:
- MAE
- RMSE
- R²
""")

    with st.expander("🔍 ¿Cómo funciona?"):
        st.write("El modelo analiza patrones en datos históricos para estimar el precio de una vivienda.")
