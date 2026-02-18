import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN
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
    # Detección flexible de la columna de estado
    col_estado = next((c for c in row.index if 'ESTADO' in c.upper()), None)
    if col_estado:
        valor = str(row[col_estado]).strip().upper()
        if valor == 'ADJUDICADA':
            return ['background-color: #fee2e2; color: #991b1b'] * len(row)
        elif valor == 'DISPONIBLE':
            return ['background-color: ; color: #065f46'] * len(row)
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

# 4. PROCESAMIENTO Y FILTROS
URL_SHEET = "https://docs.google.com/spreadsheets/d/1X78ctrqUH58bpjj57ibWucgpGrrw4NAG/edit?usp=sharing&ouid=102196281229150253520&rtpof=true&sd=true"

try:
    df = cargar_datos(URL_SHEET)

    # --- SECCIÓN DE FILTROS ---
    st.write("### 🔍 Busqueda Avanzada")
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        # Filtro NIVEL EDUCATIVO (Busca columnas que contengan 'NIVEL')
        col_nivel = next((c for c in df.columns if 'NIVEL' in c.upper()), None)
        if col_nivel:
            lista_niveles = ["TODOS"] + sorted(df[col_nivel].dropna().unique().tolist())
            nivel_sel = st.selectbox("Nivel Educativo:", lista_niveles)
            if nivel_sel != "TODOS":
                df = df[df[col_nivel] == nivel_sel]
        else:
            st.warning("Columna 'NIVEL' no encontrada")

    with c2:
        # Filtro CARGO (Busca columnas que contengan 'CARGO')
        col_cargo = next((c for c in df.columns if 'CARGO' in c.upper()), None)
        if col_cargo:
            lista_cargos = ["TODOS"] + sorted(df[col_cargo].dropna().unique().tolist())
            cargo_sel = st.selectbox("Cargo:", lista_cargos)
            if cargo_sel != "TODOS":
                df = df[df[col_cargo] == cargo_sel]
        else:
            st.warning("Columna 'CARGO' no encontrada")

    with c3:
        # Buscador General
        busqueda = st.text_input("Búsqueda por IE y/o Especialidad:", placeholder="Escriba aquí...")
        if busqueda:
            df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # --- APLICAR ESTILO Y MOSTRAR ---
    if not df.empty:
        styled_df = df.style.apply(estilo_fila, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=550, hide_index=True)
    else:
        st.info("No se encontraron plazas con los filtros seleccionados.")

except Exception as e:
    st.error(f"Error en la sincronización: {e}")

# 5. PIE DE PÁGINA Y REFRESCO
st.markdown('<div class="footer">© 2026 Equipo de Informatica - UGEL Cusco</br>Este tablero es meramente informativo.</br>La adjudicación oficial se realiza en acto público </div>', unsafe_allow_html=True)
time.sleep(3)
st.rerun()
