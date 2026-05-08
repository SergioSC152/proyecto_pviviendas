import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim
import os
import base64

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")
# ===================== CONFIG =====================
st.set_page_config(
    page_title="SMART HOME PRICE",
    page_icon="logo2.png",
    layout="wide"
)

# ===================== ESTILOS AIRBNB =====================
st.markdown("""
<style>

/* Fondo general */
body {
    background-color: #F7F7F7;
}

/* Contenedor principal */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* Botones estilo Airbnb */
.stButton>button {
    background-color: #FF5A5F;
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}

/* Hover botón */
.stButton>button:hover {
    background-color: #e0484d;
    transform: scale(1.03);
}

/* Inputs */
input, .stNumberInput input {
    border-radius: 10px !important;
    border: 1px solid #E5E7EB !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    border-radius: 10px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
}

/* Cards (para que combines luego) */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
}

/* Animación suave */
* {
    transition: all 0.2s ease-in-out;
}

</style>
""", unsafe_allow_html=True)
# ===================== HEADER PRO =====================
import streamlit.components.v1 as components

components.html(f"""
<style>
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>

<div style='
    display:flex;
    align-items:center;
    justify-content:center;
    gap:20px;
    padding: 25px;
    border-radius:20px;
    background: linear-gradient(135deg, #FF5A5F, #FF8A65);
    color:white;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
    animation: fadeIn 1s ease-in-out;
'>
    <img src="data:image/png;base64,{logo_base64}" 
         width="60"
         style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));">

    <div style="text-align:left;">
        <h1 style='margin:0; letter-spacing:1px;'>SMART HOME PRICE</h1>
        <p style='margin:0;'>Predicción inteligente de precios con IA</p>
    </div>
</div>
""", height=160)

st.divider()
# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;'>
    """, unsafe_allow_html=True)

    st.image("logo2.png", width=200)

    st.markdown("</div>", unsafe_allow_html=True)

    

    st.header("⚙️ Configura tu vivienda")

    area = int(st.text_input("📐 Área (m²)", "120"))
    cuartos = st.number_input("🛏️ Habitaciones", 1, 20, 3)
    banos = st.number_input("🚿 Baños", 1, 10, 2)
    garaje = st.number_input("🚗 Garajes", 0, 10, 1)

    calidad = st.selectbox("⭐ Calidad", ["Mala", "Regular", "Buena", "Excelente", "Lujo"])
    anio = int(st.text_input("Año de construcción", "2005"))
    ubicacion = st.selectbox("📍 Ubicación", ["Centro", "Norte", "Sur", "Suburbio"])

    st.divider()

    predecir_btn = st.button("🚀 Predecir Precio", use_container_width=True)
# ===================== MAPA =====================
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
            direccion_completa = f"{direccion}, Mazatlán, Sinaloa, México"

            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{direccion_completa}.json"

            params = {
                "access_token": st.secrets["MAPBOX_API_KEY"],
                "limit": 1
            }

            response = requests.get(url, params=params)
            data = response.json()

            if data["features"]:
                coords = data["features"][0]["center"]
                lon, lat = coords[0], coords[1]

                st.session_state.map_data = pd.DataFrame({
                    "lat": [lat],
                    "lon": [lon]
                })

                st.success(f"📍 {data['features'][0]['place_name']}")
            else:
                st.error("❌ No se encontró la dirección")

        except Exception as e:
            st.error(f"❌ Error: {e}")
    # MAPA
import os
import pydeck as pdk

token = st.secrets["MAPBOX_API_KEY"]

lat = st.session_state.map_data["lat"][0]
lon = st.session_state.map_data["lon"][0]

# 🔥 DATA CON ICONO REAL
data = [{
    "lat": lat,
    "lon": lon,
    "icon_data": {
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }
}]

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=15,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "IconLayer",
            data=data,
            get_icon="icon_data",  # 🔥 AQUÍ ESTÁ LA CLAVE
            get_size=4,
            size_scale=15,
            get_position='[lon, lat]',
            pickable=True,
        ),
    ],
    tooltip={
        "text": "📍 Ubicación seleccionada"
    }
))

    # ===================== RESULTADO PRO =====================
import streamlit.components.v1 as components  # 👈 asegúrate de tener esto arriba

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

            factor = factores[ubicacion]
            precio = precio_base * factor
            precio_mxn = precio * 17

            st.balloons()

            # 🔥 CARDS PRO (AHORA SÍ FUNCIONAN)
            components.html(f"""
            <style>
            @keyframes fadeCard {{
                from {{opacity:0; transform: translateY(20px);}}
                to {{opacity:1; transform: translateY(0);}}
            }}
            </style>

            <div style='
                display:flex;
                justify-content:space-around;
                gap:20px;
                margin-top:25px;
            '>

                <div style='
                    background:white;
                    padding:25px;
                    border-radius:18px;
                    text-align:center;
                    width:30%;
                    box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
                    animation: fadeCard 0.6s ease;
                '>
                    <h4>💰 Precio USD</h4>
                    <h2 style="color:#FF5A5F;">${precio:,.2f}</h2>
                </div>

                <div style='
                    background:white;
                    padding:25px;
                    border-radius:18px;
                    text-align:center;
                    width:30%;
                    box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
                    animation: fadeCard 0.8s ease;
                    animation-delay: 0.2s;
                '>
                    <h4>🇲🇽 Precio MXN</h4>
                    <h2 style="color:#FF5A5F;">${precio_mxn:,.2f}</h2>
                </div>

                <div style='
                    background:white;
                    padding:25px;
                    border-radius:18px;
                    text-align:center;
                    width:30%;
                    box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
                    animation: fadeCard 1s ease;
                '>
                    <h4>📍 Ubicación</h4>
                    <h2>{ubicacion}</h2>
                </div>

            </div>
            """, height=230)

            st.info(f"📍 Factor de ubicación aplicado: x{factor}")
            st.progress(92)

        else:
            st.error("❌ Error en backend")

    except Exception as e:
        st.error(f"❌ Error: {e}")