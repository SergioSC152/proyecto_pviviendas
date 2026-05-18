import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import os
import base64
import pydeck as pdk
import streamlit.components.v1 as components

# ===================== CONFIGURACIÓN INICIAL =====================
st.set_page_config(
    page_title="SMART HOME PRICE",
    page_icon="logo2.png",
    layout="wide"
)

def get_base64_image(path):
    try:
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except FileNotFoundError:
        return ""

logo_base64 = get_base64_image("logo.png")

# ===================== ESTILOS CSS GENERALES =====================
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background-color: #F5F7FA;
}

/* Contenedor principal */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A5F, #2DD4D7);
    color: white;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p {
    color: white !important;
}

/* Botones */
.stButton>button {
    background: linear-gradient(135deg, #1E3A5F, #2DD4D7);
    color: white;
    border: none;
    border-radius: 14px;
    height: 3.2em;
    font-weight: bold;
    transition: 0.3s;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0px 12px 25px rgba(0,0,0,0.25);
}

/* Inputs generales */
.stTextInput input, .stNumberInput input, .stSelectbox div {
    border-radius: 12px !important;
    color: #111827 !important;
    background-color: white !important;
}

/* Labels del cuerpo principal (Fondo claro) - Texto oscuro */
.block-container label, 
.block-container .stSelectbox label, 
.block-container .stTextInput label, 
.block-container .stNumberInput label {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* ELIMINAR CÁPSULAS BLANCAS EN EL SIDEBAR (SOLUCIÓN DEFINITIVA) */
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"],
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] div,
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    background: transparent !important;
    background-color: transparent !important;
    text-shadow: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Contenedor unificado para buscador y mapa */
.main-card {
    background-color: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.05);
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER PREMIUM =====================
components.html(f"""
<div style='display:flex; align-items:center; justify-content:center; gap:25px; padding:30px; border-radius:25px; background: linear-gradient(135deg, #1E3A5F, #2DD4D7); color:white; box-shadow: 0px 15px 35px rgba(0,0,0,0.20);'>
    <img src="data:image/png;base64,{logo_base64}" width="85" style="filter: drop-shadow(0px 5px 10px rgba(0,0,0,0.30));">
    <div style="text-align:left;">
        <h1 style='margin:0; letter-spacing:1px; font-size:42px; font-weight:800;'>SMART HOME PRICE</h1>
        <p style='margin:0; font-size:18px; opacity:0.92;'>Predicción inteligente de precios con IA</p>
    </div>
</div>
""", height=150)

# ===================== CARGA DE DATOS Y LÓGICA =====================
@st.cache_data
def cargar_datos():

    zonas = pd.read_csv("../data/zonas_mazatlan.csv")

    coords = pd.read_csv("../data/zonas_coords.csv")

    return zonas, coords

zonas_df, coords_df = cargar_datos()

def detectar_zona(lat_usuario, lon_usuario):
    distancia_minima = float("inf")
    zona_detectada = None
    for _, row in coords_df.iterrows():
        distancia = geodesic((lat_usuario, lon_usuario), (row["lat"], row["lon"])).kilometers
        if distancia < distancia_minima:
            distancia_minima = distancia
            zona_detectada = row["zona"]
    return zona_detectada

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;'>
    """, unsafe_allow_html=True)

    st.image("logo2.png", width=180)

    st.markdown("</div>", unsafe_allow_html=True)

    st.header("⚙️ Configura tu vivienda")

    # Inputs estándar (Tienen suficiente texto nativo, se quedan igual)
    area = int(st.text_input("📐 Área (m²)", "120"))
    cuartos = st.number_input("🛏️ Habitaciones", 1, 20, 3)
    banos = st.number_input("🚿 Baños", 1, 10, 2)
    garaje = st.number_input("🚗 Garajes", 0, 10, 1)

    # 1. Selector de Calidad (Con contenedor HTML para dar espacio arriba y abajo)
    st.markdown("""
        <div style='margin-top: 15px; margin-bottom: 5px;'>
            <label style='color: white !important; font-weight: 600; font-size: 16px;'>⭐ Calidad</label>
        </div>
    """, unsafe_allow_html=True)
    calidad = st.selectbox(
        "Calidad_hidden", 
        ["Mala", "Regular", "Buena", "Excelente", "Lujo"],
        label_visibility="collapsed"
    )
    
    # Input estándar
    anio = int(st.text_input("Año de construcción", "2005"))
    
    # Lógica de zona por defecto
    zona_default = st.session_state.get("zona_detectada", zonas_df["zona"].tolist()[0])
    try:
        idx_default = zonas_df["zona"].tolist().index(zona_default)
    except ValueError:
        idx_default = 0

    # 2. Selector de Zona (Con espacio controlado)
    st.markdown("""
        <div style='margin-top: 15px; margin-bottom: 5px;'>
            <label style='color: white !important; font-weight: 600; font-size: 16px;'>📍 Zona de Mazatlán</label>
        </div>
    """, unsafe_allow_html=True)
    zona = st.selectbox(
        "Zona_hidden",
        zonas_df["zona"].tolist(),
        index=idx_default,
        label_visibility="collapsed"
    )

    # 3. Selector de Tipo de Propiedad (Con espacio controlado)
    st.markdown("""
        <div style='margin-top: 15px; margin-bottom: 5px;'>
            <label style='color: white !important; font-weight: 600; font-size: 16px;'>🏠 Tipo de propiedad</label>
        </div>
    """, unsafe_allow_html=True)
    tipo_propiedad = st.selectbox(
        "Tipo_hidden",
        ["Casa", "Departamento"],
        label_visibility="collapsed"
    )

    st.divider()

    predecir_btn = st.button("🚀 Predecir Precio", use_container_width=True)

# ===================== CUERPO PRINCIPAL =====================
if "map_data" not in st.session_state:
    st.session_state.map_data = pd.DataFrame({"lat": [23.2494], "lon": [-106.4111]})
if "direccion" not in st.session_state:
    st.session_state.direccion = "Calle Simón Bolívar 622"

# CONTENEDOR UNIFICADO DEL BUSCADOR Y EL MAPA
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.subheader("🗺️ Ubicación del inmueble")

# Grid horizontal para Buscador
col_input, col_btn = st.columns([4, 1])
with col_input:
    direccion = st.text_input("Ingresa la dirección", value=st.session_state.direccion, label_visibility="collapsed")
with col_btn:
    buscar_btn = st.button("Buscar ubicación", use_container_width=True)

# Lógica del Buscador
if buscar_btn and direccion:
    st.session_state.direccion = direccion
    try:
        direccion_completa = f"{direccion}, Mazatlán, Sinaloa, México"
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{direccion_completa}.json"
        params = {"access_token": st.secrets["MAPBOX_API_KEY"], "limit": 1}
        
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("features"):
            coords = data["features"][0]["center"]
            lon, lat = coords[0], coords[1]
            zona_detectada = detectar_zona(lat, lon)

            st.session_state.map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
            st.session_state.direccion_encontrada = data['features'][0]['place_name']
            st.session_state.zona_detectada = zona_detectada
            st.rerun()
        else:
            st.error("❌ No se encontró la dirección")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Información de Texto Inline (Reemplazo de Alertas gigantes)
if "direccion_encontrada" in st.session_state:
    st.markdown(f"""
    <p style='margin: 8px 0 2px 0; color: #374151; font-size: 14px;'><strong>📍 Dirección:</strong> {st.session_state.direccion_encontrada}</p>
    <p style='margin: 0 0 15px 0; color: #1E3A5F; font-size: 14px;'><strong>🏠 Zona Detectada:</strong> {st.session_state.zona_detectada}</p>
    """, unsafe_allow_html=True)

# Render del Mapa PyDeck
lat = st.session_state.map_data["lat"][0]
lon = st.session_state.map_data["lon"][0]

mapa_marcador = [{
    "lat": lat, "lon": lon,
    "icon_data": {"url": "https://cdn-icons-png.flaticon.com/512/684/684908.png", "width": 128, "height": 128, "anchorY": 128}
}]

st.pydeck_chart(
    pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=15, pitch=45),
        layers=[pdk.Layer("IconLayer", data=mapa_marcador, get_icon="icon_data", get_size=4, size_scale=15, get_position='[lon, lat]', pickable=True)],
        tooltip={"text": "📍 Ubicación seleccionada"}
    ),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ===================== LÓGICA DE PREDICCIÓN IA =====================
if predecir_btn:
    try:
        
        payload = {
         "area": area,
         "habitaciones": cuartos,
         "banos": banos,
         "garaje": garaje,
         "calidad": calidad,
         "zona": zona,
         "tipo": tipo_propiedad,
         "anio": anio
         }

        response = requests.post(
            "http://127.0.0.1:5000/predecir",
            json=payload
        )
        
        if response.status_code == 200:
            precio_mxn = response.json()["precio"]
             
            st.session_state.precio = precio_mxn / 17
            st.session_state.precio_mxn = precio_mxn
            st.session_state.zona_final = zona

            st.balloons()
        else:
            st.error("❌ Error en backend")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ===================== TARJETAS DE RESULTADOS INTERIORES =====================
if "precio_mxn" in st.session_state:
    components.html(f"""
    <div style='display:flex; justify-content:space-between; gap:20px; margin-top:10px;'>
        <div style='background:white; padding:20px; border-radius:16px; text-align:center; flex:1; box-shadow:0px 10px 25px rgba(0,0,0,0.06); font-family: sans-serif;'>
            <h4 style="margin:0; color:#6B7280; font-size:14px;">💰 Precio USD</h4>
            <h2 style="color:#1E3A5F; margin:10px 0 0 0; font-size:28px; font-weight:700;">${st.session_state.precio:,.2f}</h2>
        </div>
        <div style='background:white; padding:20px; border-radius:16px; text-align:center; flex:1; box-shadow:0px 10px 25px rgba(0,0,0,0.06); font-family: sans-serif;'>
            <h4 style="margin:0; color:#6B7280; font-size:14px;">🇲🇽 Precio MXN</h4>
            <h2 style="color:#2DD4D7; margin:10px 0 0 0; font-size:28px; font-weight:700;">${st.session_state.precio_mxn:,.2f}</h2>
        </div>
        <div style='background:white; padding:20px; border-radius:16px; text-align:center; flex:1; box-shadow:0px 10px 25px rgba(0,0,0,0.06); font-family: sans-serif;'>
            <h4 style="margin:0; color:#6B7280; font-size:14px;">📍 Ubicación Seleccionada</h4>
            <h2 style="color:#111827; margin:10px 0 0 0; font-size:24px; font-weight:700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{st.session_state.zona_final}</h2>
        </div>
    </div>
    """, height=120)