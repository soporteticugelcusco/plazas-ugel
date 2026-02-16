import streamlit as st
import pandas as pd
import time

# Configuración de página
st.set_page_config(page_title="Adjudicación de Plazas en Vivo", layout="wide")

# Estilo para que se vea profesional
st.markdown("""
    <style>
    .stApp { background-color: #f5f7f9; }
    .status-viva { color: #28a745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📋 Seguimiento de Adjudicación de Plazas")
st.markdown(f"**Estado:** <span class='status-viva'>● EN VIVO</span>", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LA BASE ---
# Reemplaza con tu link de Google Sheets
URL_SHEET = "https://docs.google.com/spreadsheets/d/1E1bGvrOn6vmYZxIlRYZfqdQ8DiYXJBtH/edit?usp=sharing&ouid=102196281229150253520&rtpof=true&sd=true"

# --- CARGA DE DATOS CON CACHÉ DE 3 SEGUNDOS ---
@st.cache_data(ttl=3)
def cargar_plazas(url):
    # Transformamos el link para descarga directa en CSV
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

try:
    df = cargar_plazas(URL_SHEET)

    # Buscador rápido
    busqueda = st.text_input("🔍 Buscar plaza, institución o estado:", placeholder="Escribe aquí...")

    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # Mostrar la tabla
    st.dataframe(df, use_container_width=True, height=500)

    # --- AUTO-REFRESCO VISUAL ---
    # Esto obliga al navegador a pedir datos nuevos cada 3 segundos
    time.sleep(3)
    st.rerun()

except Exception as e:
    st.error("Conectando con el servidor de datos...")
    time.sleep(2)
    st.rerun()
