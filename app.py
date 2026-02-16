import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Adjudicación UGEL Cusco", page_icon="🎓", layout="wide")

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
    [data-testid="stMetricValue"] { font-size: 28px; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES
@st.cache_data(ttl=3)
def cargar_datos(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

def aplicar_color_fila(row):
    # Buscamos la columna de estado sin importar si es 'ESTADO' o 'Estado'
    col_estado = 'ESTADO' if 'ESTADO' in row.index else 'Estado'
    val = str(row[col_estado]).strip().upper()
    
    if val == 'DISPONIBLE':
        return ['background-color: #d1fae5; color: #065f46'] * len(row)
    elif val == 'ADJUDICADA':
        return ['background-color: #fee2e2; color: #991b1b'] * len(row)
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

# 4. DATOS Y MÉTRICAS
URL_SHEET = "https://docs.google.com/spreadsheets/d/1E1bGvrOn6vmYZxIlRYZfqdQ8DiYXJBtH/edit?usp=sharing"

try:
    df = cargar_datos(URL_SHEET)
    
    # Identificar columna de estado
    col_e = 'ESTADO' if 'ESTADO' in df.columns else 'Estado'

    # --- NUEVA SECCIÓN: CONTADORES ---
    if col_e in df.columns:
        m1, m2, m3 = st.columns(3)
        total = len(df)
        adj = len(df[df[col_e].str.strip().str.upper() == 'ADJUDICADA'])
        disp = len(df[df[col_e].str.strip().str.upper() == 'DISPONIBLE'])
        
        m1.metric("TOTAL PLAZAS", total)
        m2.metric("ADJUDICADAS ✅", adj, delta=f"{(adj/total)*100:.1f}%", delta_color="normal")
        m3.metric("DISPONIBLES ⏳", disp, delta=f"-{total-adj}", delta_color="inverse")
    
    st.divider()

    # Buscador
    busqueda = st.text_input("🔍 Buscar por Institución, Modalidad o Código:", placeholder="Escriba para filtrar...")
    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]

    # APLICAR COLORES A TODA LA FILA
    if col_e in df.columns:
        styled_df = df.style.apply(aplicar_color_fila, axis=1)
    else:
        styled_df = df

    st.dataframe(styled_df, use_container_width=True, height=500, hide_index=True)

except Exception as e:
    st.warning("🔄 Sincronizando datos...")

# 5. PIE DE PÁGINA Y REFRESCO
st.markdown('<div class="footer">© 2026 UGEL Cusco - Equipo de Informática. El tablero se refresca automáticamente.</div>', unsafe_allow_html=True)
time.sleep(3)
st.rerun()
