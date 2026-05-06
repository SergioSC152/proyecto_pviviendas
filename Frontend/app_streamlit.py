import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim
import pydeck as pdk

# ===================== CONFIG =====================
st.set_page_config(
    page_title="SMART HOME PRICE",
    page_icon="logo2.png",
    layout="wide"
)

st.title("🏠 SMART HOME PRICE")
st.info("💡 Ingresa las características del inmueble y obtén una estimación.")

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("⚙️ Configura tu vivienda")

    area = int(st.text_input("📐 Área (m²)", "120"))

    cuartos = st.number_input("🛏️ Habitaciones", 1, 20, 3)
    banos = st.number_input("🚿 Baños", 1, 10, 2)
    garaje = st.number_input("🚗 Garajes", 0, 10, 1)

    calidad = st.selectbox("⭐ Calidad", ["Mala", "Regular", "Buena", "Excelente", "Lujo"])

    anio = int(st.text_input("Año de construcción", "2005"))

    ubicacion = st.selectbox("📍 Ubicación", ["Centro", "Norte", "Sur", "Suburbio"])

    predecir_btn = st.button("🔮 Predecir Precio")

# ===================== ESTADO MAPA =====================
if "map_data" not in st.session_state:
    st.session_state.map_data = pd.DataFrame({
        "lat": [23.2494],
        "lon": [-106.4111]
    })

# ===================== TABS =====================
tab1, tab2, tab3 = st.tabs(["📊 Predicción", "📈 Visualización", "🧠 Modelo"])

# ===================== TAB 1 =====================
with tab1:
    st.subheader("🗺️ Ubicación del inmueble")

    direccion = st.text_input("📍 Ingresa la dirección", "Mazatlán, Sinaloa")
    buscar_btn = st.button("Buscar ubicación")

    if buscar_btn:
        try:
            geolocator = Nominatim(user_agent="smart_home_app")

            # 🔥 Forzar búsqueda en Mazatlán
            direccion_completa = f"{direccion}, Mazatlán, Sinaloa, México"

            location = geolocator.geocode(direccion_completa)

            if location:
                st.session_state.map_data = pd.DataFrame({
                    "lat": [location.latitude],
                    "lon": [location.longitude]
                })

                st.success(f"📍 {location.address}")
            else:
                st.error("❌ No se encontró la dirección")

        except Exception as e:
            st.error(f"❌ Error: {e}")

    # ===================== MAPA PRO =====================
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",  # 🔥 MAPA A COLOR
        initial_view_state=pdk.ViewState(
            latitude=st.session_state.map_data["lat"][0],
            longitude=st.session_state.map_data["lon"][0],
            zoom=13,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=st.session_state.map_data,
                get_position='[lon, lat]',
                get_radius=250,
                get_fill_color=[0, 200, 255],  # 🔥 azul tipo Google
            ),
        ],
    ))

    st.divider()

    # ===================== PREDICCIÓN =====================
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
                "habitaciones": cuartos,
                "banos": banos,
                "garaje": garaje,
                "anio": anio
            }

            response = requests.post("http://127.0.0.1:5000/predecir", json=data)

            if response.status_code == 200:
                precio_base = response.json()["precio"]

                factores = {
                    "Centro": 1.25,
                    "Norte": 1.15,
                    "Sur": 0.95,
                    "Suburbio": 0.85
                }

                precio = precio_base * factores[ubicacion]
                precio_mxn = precio * 17

                st.success(f"💰 USD: ${precio:,.2f}")
                st.success(f"🇲🇽 MXN: ${precio_mxn:,.2f}")

            else:
                st.error("❌ Error en backend")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ===================== TAB 2 =====================
with tab2:
    st.subheader("📊 Visualización")
    st.bar_chart([120000, 150000, 170000, 140000])

# ===================== TAB 3 =====================
with tab3:
    st.subheader("🧠 Modelo")
    st.write("Modelo: Random Forest")
    st.write("Variables: Área, Habitaciones, Baños, Garajes, Calidad, Año")
