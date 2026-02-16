import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Adjudicación de Plazas - Contrata Docente - En Vivo",
    page_icon="📋",
    layout="wide"
)

# 2. ESTILOS PERSONALIZADOS (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #003366;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 100;
    }
    .header-container {
        display: flex;
        align-items: center;
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .status-live {
        color: #d9534f;
        font-weight: bold;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA CON LOGOTIPO
with st.container():
    col_logo, col_titulo = st.columns([1, 4])
    with col_logo:
        # REEMPLAZA ESTA URL CON EL LOGO OFICIAL DE LA UGEL
        logo_url = "https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png" 
        st.image(logo_url, width=150)
    
    with col_titulo:
        st.subheader("UNIDAD DE GESTIÓN EDUCATIVA LOCAL CUSCO")
        st.title("ADJUDICACIÓN DE PLAZAS CONTRATO DOCENTE")
        st.markdown("<span class='status-live'>● Transmisión en vivo (CADA 3s)</span>", unsafe_allow_html=True)

st.divider()

# 4. LÓGICA DE DATOS (Mantiene los 3 segundos de caché)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1E1bGvrOn6vmYZxIlRYZfqdQ8DiYXJBtH/edit?usp=sharing&ouid=102196281229150253520&rtpof=true&sd=true"

@st.cache_data(ttl=3)
def cargar_datos(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

try:
    df = cargar_datos(URL_SHEET)

    # Filtros rápidos
    c1, c2 = st.columns([2, 1])
    with c1:
        busqueda = st.text_input("🔍 Buscar por Institución, Cargo o Distrito:", placeholder="Ej. Colegio Nacional...")
    with c2:
        # Si tienes una columna llamada 'Estado', esto ayuda mucho
        if 'Estado' in df.columns:
            opciones = ["TODAS"] + list(df['Estado'].unique())
            filtro_estado = st.selectbox("Filtrar por Estado:", opciones)
            if filtro_estado != "TODAS":
                df = df[df['Estado'] == filtro_estado]

    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # Visualización de la tabla
    st.dataframe(df, use_container_width=True, height=500, hide_index=True)

except Exception as e:
    st.info("🔄 Sincronizando datos con la base central... espere un momento.")

# 5. PIE DE PÁGINA PERSONALIZADO
st.markdown("""
    <div class="footer">
        <p>© 2026 - Equipo de Informática - UGEL Cusco. 
        Este tablero es meramente informativo. La adjudicación oficial se realiza en acto público.</p>
    </div>
    """, unsafe_allow_html=True)

# 6. AUTO-REFRESCO
time.sleep(3)
st.rerun()
