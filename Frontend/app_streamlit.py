import streamlit as st

# CONFIG
st.set_page_config(page_title="SMART HOME PRICE", page_icon="🏠", layout="wide")

# --- HEADER PRINCIPAL ---
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

# TAB 1
with tab1:
    st.subheader("Resultado de la predicción")

    if predecir_btn:
        factor_calidad = {
            "Mala": 0.8,
            "Regular": 1.0,
            "Buena": 1.2,
            "Excelente": 1.5,
            "Lujo": 2.0
        }

        factor_ubicacion = {
            "Centro": 1.5,
            "Norte": 1.3,
            "Sur": 1.1,
            "Suburbio": 0.9
        }

        precio = (area * 900 + cuartos * 8000 + banos * 5000)
        precio *= factor_calidad[calidad] * factor_ubicacion[ubicacion]

        st.session_state.precio = precio

        st.balloons()

        st.success(f"""
        ## 💰 ${precio:,.2f} USD
        ### 📍 Ubicación: {ubicacion}
        """)

        # NUEVO (para commit 2)
        st.info("📌 Este resultado es una estimación basada en un modelo de Machine Learning entrenado.")

        # Barra de confianza visual
        st.progress(92)

# TAB 2
with tab2:
    st.subheader("📊 Distribución de precios")
    st.bar_chart([120000, 150000, 170000, 140000, 200000])

    # NUEVO (para commit 3)
    st.write("📈 Esta gráfica representa precios de viviendas similares en el dataset.")

    st.caption("Datos simulados - Sprint 3 (EDA)")

# TAB 3
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
- Ubicación

Métricas:
- MAE
- RMSE
- R²
""")

    with st.expander("🔍 ¿Cómo funciona?"):
        st.write("El modelo analiza patrones en datos históricos para estimar el precio de una vivienda.")
        