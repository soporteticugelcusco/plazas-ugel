import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Adjudicación de Plazas - Contrata Docente - UGEL Cusco",
    page_icon="🎓",
    layout="wide"
)

# 2. ESTILOS CSS PARA EL DISEÑO Y PIE DE PÁGINA
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

# 3. CABECERA INSTITUCIONAL
with st.container():
    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        # Puedes usar una URL o un archivo local 'logo.png'
        st.image("https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png", width=140)
    with col_titulo:
        st.subheader("UNIDAD DE GESTIÓN EDUCATIVA LOCAL CUSCO")
        st.title("ADJUDICACIÓN DE PLAZAS CONTRATO DOCENTE")
        st.markdown("<span class='status-live'>● ACTUALIZACIÓN (CADA 3s)</span>", unsafe_allow_html=True)

st.divider()

# 4. FUNCIÓN PARA COLOREAR FILAS
def color_estado(val):
    # Asume que tu columna se llama 'Estado'
    # Ajusta los nombres 'DISPONIBLE' o 'ADJUDICADA' según tu Excel
    color = ''
    if str(val).upper() == 'DISPONIBLE':
        color = 'background-color: #d1fae5; color: #065f46' # Verde claro
    elif str(val).upper() == 'ADJUDICADA':
        color = 'background-color: #fee2e2; color: #991b1b' # Rojo claro
    return color

# 5. CARGA DE DATOS (TTL = 3 segundos)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1E1bGvrOn6vmYZxIlRYZfqdQ8DiYXJBtH/edit?usp=sharing&ouid=102196281229150253520&rtpof=true&sd=true"

@st.cache_data(ttl=3)
def cargar_datos(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

try:
    df = cargar_datos(URL_SHEET)

    # Buscador interactivo
    busqueda = st.text_input("🔍 Buscar por Institución Educativa:", placeholder="Escriba para filtrar...")

    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # APLICAR ESTILOS A LA TABLA
    # Si tienes una columna 'Estado', se aplicará el color a esa celda
    if 'Estado' in df.columns:
        styled_df = df.style.applymap(color_estado, subset=['Estado'])
    else:
        styled_df = df

    # Mostrar la tabla estilizada
    st.dataframe(styled_df, use_container_width=True, height=550, hide_index=True)

except Exception as e:
    st.warning("🔄 Sincronizando con la base de datos de plazas...")

# 6. PIE DE PÁGINA
st.markdown("""
    <div class="footer">
        © 2026 UGEL Cusco- Equipo de Informática. 
        </br>Este tablero es meramente informativo. 
        </br>La adjudicación oficial se realiza en acto público
    </div>
    """, unsafe_allow_html=True)

# 7. LOGICA DE REFRESCO
time.sleep(3)
st.rerun()
