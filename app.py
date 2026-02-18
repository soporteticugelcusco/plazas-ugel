import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN (Icono personalizado con URL)
st.set_page_config(
    page_title="Adjudicación UGEL Cusco", 
    page_icon="https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png", 
    layout="wide"
)

# Estilos CSS
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

# 2. FUNCIONES
@st.cache_data(ttl=3)
def cargar_datos(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

def estilo_fila(row):
    col_estado = 'ESTADO' if 'ESTADO' in row.index else 'Estado'
    valor = str(row[col_estado]).strip().upper()
    if valor == 'ADJUDICADA':
        return ['background-color: #fee2e2; color: #991b1b'] * len(row)
    elif valor == 'DISPONIBLE':
        return ['background-color: #d1fae5; color: #065f46'] * len(row)
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

st.divider()

# 4. PROCESAMIENTO DE DATOS Y FILTROS
URL_SHEET = "https://docs.google.com/spreadsheets/d/1X78ctrqUH58bpjj57ibWucgpGrrw4NAG/edit?usp=sharing&ouid=102196281229150253520&rtpof=true&sd=true"

try:
    df = cargar_datos(URL_SHEET)

    # --- SECCIÓN DE FILTROS ---
    st.write("### 🔍 Filtrar Plazas")
    c1, c2, c3 = st.columns([1, 1, 2])
    
    with c1:
        # Filtro Nivel Educativo (Asegúrate que la columna se llame 'NIVEL')
        col_nivel = 'NIVEL' if 'NIVEL' in df.columns else 'Nivel'
        if col_nivel in df.columns:
            lista_niveles = ["TODOS"] + sorted(df[col_nivel].dropna().unique().tolist())
            nivel_sel = st.selectbox("Seleccione Nivel:", lista_niveles)
            if nivel_sel != "TODOS":
                df = df[df[col_nivel] == nivel_sel]

    with c2:
        # Filtro Cargo (Asegúrate que la columna se llame 'CARGO')
        col_cargo = 'CARGO' if 'CARGO' in df.columns else 'Cargo'
        if col_cargo in df.columns:
            lista_cargos = ["TODOS"] + sorted(df[col_cargo].dropna().unique().tolist())
            cargo_sel = st.selectbox("Seleccione Cargo:", lista_cargos)
            if cargo_sel != "TODOS":
                df = df[df[col_cargo] == cargo_sel]

    with c3:
        # Buscador General
        busqueda = st.text_input("Búsqueda Rápida (IE, Distrito, DNI):", placeholder="Escriba aquí...")
        if busqueda:
            df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # --- APLICAR ESTILO Y MOSTRAR ---
    styled_df = df.style.apply(estilo_fila, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=500, hide_index=True)

except Exception as e:
    st.warning("🔄 Sincronizando datos con la central...")

# 5. PIE DE PÁGINA Y REFRESCO
st.markdown('<div class="footer">© 2026 UGEL Cusco - El tablero se refresca automáticamente cada 3s.</div>', unsafe_allow_html=True)
time.sleep(3)
st.rerun()
