import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Adjudicación UGEL Cusco", page_icon="🎓", layout="wide")

# Estilos CSS (Mantenemos el pie de página y el parpadeo)
st.markdown("""
    <style>
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #1e3a8a; color: white; text-align: center;
        padding: 8px; font-size: 13px; z-index: 100;
    }
    .status-live { color: #ef4444; font-weight: bold; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.2; } }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE DATOS
@st.cache_data(ttl=2)
def cargar_datos(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

# --- ESTA ES LA FUNCIÓN CLAVE PARA PINTAR TODA LA FILA ---
def estilo_fila(row):
    # Buscamos la columna de estado ignorando mayúsculas/minúsculas
    col_estado = 'ESTADO' if 'ESTADO' in row.index else 'Estado'
    valor = str(row[col_estado]).strip().upper()
    
    if valor == 'ADJUDICADA':
        # Rojo claro para toda la fila
        return ['background-color: #FFFF99; color: #000000'] * len(row)
    elif valor == 'DISPONIBLE':
        # Verde claro para toda la fila
        return ['background-color: #6CD900; color: #000000'] * len(row)
    return [''] * len(row)

# 3. CABECERA
with st.container():
    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        st.image("https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png", width=140)
    with col_titulo:
        st.subheader("UNIDAD DE GESTIÓN EDUCATIVA LOCAL CUSCO")
        st.title("ADJUDICACIÓN DE PLAZAS CONTRATO DOCENTE")
        st.markdown("<span class='status-live'>● ACTUALIZACIÓN EN VIVO (CADA 3s)</span>", unsafe_allow_html=True)

# 4. PROCESAMIENTO DE TABLA
URL_SHEET = "https://docs.google.com/spreadsheets/d/1E1bGvrOn6vmYZxIlRYZfqdQ8DiYXJBtH/edit?usp=sharing"

try:
    df = cargar_datos(URL_SHEET)

    # Buscador
    busqueda = st.text_input("🔍 Buscar por Institución, Modalidad o Código:", placeholder="Escriba para filtrar...")
    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # --- APLICAR ESTILO A NIVEL DE FILA (axis=1) ---
    # Esto asegura que toda la línea se pinte
    styled_df = df.style.apply(estilo_fila, axis=1)

    # Mostrar la tabla
    st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)

except Exception as e:
    st.error(f"Error al cargar datos o aplicar estilos: {e}")

# 5. PIE DE PÁGINA Y REFRESCO
st.markdown('<div class="footer">© UGEL Cusco - Equipo de Informática 2026 </br>.</br>Este tablero es meramente informativo.</br>La adjudicación oficial se realiza en acto público </div>', unsafe_allow_html=True)

time.sleep(3)
st.rerun()
