import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Adjudicación de Plazas - UGEL Cusco",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1e3a8a;
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 13px;
        z-index: 100;
    }
    .status-live {
        color: #ef4444;
        font-weight: bold;
        animation: blinker 2s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.2; } }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DEFINICIÓN DE FUNCIONES (Primero se definen)
# ==========================================

@st.cache_data(ttl=3)
def cargar_datos(url):
    # Transformamos el link para descarga directa en CSV
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

def color_estado(val):
    estado = str(val).strip().upper()
    if estado == 'DISPONIBLE':
        return 'background-color: #d1fae5; color: #065f46' # Verde
    elif estado == 'ADJUDICADA':
        return 'background-color: #fee2e2; color: #991b1b' # Rojo
    elif estado == 'RESERVADA':
        return 'background-color: #fef3c7; color: #92400e' # Amarillo
    return ''

# ==========================================
# 3. CABECERA
# ==========================================
with st.container():
    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        st.image("https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png", width=140)
    with col_titulo:
        st.subheader("UNIDAD DE GESTIÓN EDUCATIVA LOCAL CUSCO")
        st.title("ADJUDICACIÓN DE PLAZAS CONTRATO DOCENTE")
        st.markdown("<span class='status-live'>● ACTUALIZACIÓN (CADA 3s)</span>", unsafe_allow_html=True)

st.divider()

# ==========================================
# 4. LÓGICA PRINCIPAL (Carga, Filtro y Visualización)
# ==========================================
URL_SHEET = "https://docs.google.com/spreadsheets/d/1E1bGvrOn6vmYZxIlRYZfqdQ8DiYXJBtH/edit?usp=sharing"

try:
    # Carga
    df = cargar_datos(URL_SHEET)

    # Buscador
    busqueda = st.text_input("🔍 Buscar por Institución Educativa:", placeholder="Escriba para filtrar...")
    
    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # Aplicar Colores
    # He usado 'ESTADO' en mayúsculas porque así aparece en tu imagen
    if 'ESTADO' in df.columns:
        styled_df = df.style.map(color_estado, subset=['ESTADO'])
    elif 'Estado' in df.columns:
        styled_df = df.style.map(color_estado, subset=['Estado'])
    else:
        styled_df = df

    # Mostrar Tabla
    st.dataframe(styled_df, use_container_width=True, height=550, hide_index=True)

except Exception as e:
    st.warning("🔄 Sincronizando con la base de datos de plazas...")
    st.info("Asegúrese de que el archivo de Google Sheets tenga los permisos de 'Cualquier persona con el enlace'.")

# ==========================================
# 5. PIE DE PÁGINA Y REFRESCO
# ==========================================
st.markdown("""
    <div class="footer">
        © 2026 UGEL Cusco - Equipo de Informática. <br>
        Este tablero es meramente informativo. La adjudicación oficial se realiza en acto público.
    </div>
    """, unsafe_allow_html=True)

# Pausa de 3 segundos antes de reiniciar la app para el efecto "En Vivo"
time.sleep(3)
st.rerun()
