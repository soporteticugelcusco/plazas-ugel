import streamlit as st
import pandas as pd

# ============================================================
# 1. CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="Adjudicación UGEL Cusco",
    page_icon="https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png",
    layout="wide"
)

# ============================================================
# 2. AUTO-REFRESH SIN BLOQUEAR HILOS DEL SERVIDOR
#    streamlit-autorefresh usa JavaScript del navegador,
#    NO bloquea threads con sleep() → soporta N usuarios
# ============================================================
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=15_000, limit=None, key="live_refresh")
    # interval en milisegundos → 15 segundos es suficiente
    # Google Sheets no necesita actualizarse cada 3 segundos
except ImportError:
    st.warning("⚠️ Instala: pip install streamlit-autorefresh")

# ============================================================
# 3. ESTILOS CSS
# ============================================================
st.markdown("""
    <style>
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #1e3a8a; color: white; text-align: center;
        padding: 8px; font-size: 13px; z-index: 100;
    }
    .status-live {
        color: #ef4444; font-weight: bold;
        animation: blinker 2s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.2; } }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 4. CARGA DE DATOS CON CACHE
#    TTL=30 segundos: reduce drasticamente las llamadas a
#    Google Sheets cuando hay muchos usuarios simultáneos.
#    Todos los usuarios comparten el mismo cache.
# ============================================================
@st.cache_data(ttl=30, show_spinner="Sincronizando datos...")
def cargar_datos(url: str) -> pd.DataFrame:
    """
    Carga datos desde Google Sheets.
    El cache es COMPARTIDO entre todos los usuarios:
    si 50 personas abren la app al mismo tiempo,
    Google Sheets solo recibe UNA solicitud cada 30 segundos.
    """
    csv_url = url.replace(
        "/edit?usp=sharing", "/export?format=csv"
    ).replace(
        "&ouid=102196281229150253520&rtpof=true&sd=true", ""
    )
    df = pd.read_csv(csv_url)
    # Normalizar nombres de columnas: quitar espacios extra
    df.columns = df.columns.str.strip()
    return df

def estilo_fila(row):
    col_estado = next((c for c in row.index if "ESTADO" in c.upper()), None)
    if col_estado:
        valor = str(row[col_estado]).strip().upper()
        if valor == "ADJUDICADA":
            return ["background-color: #fee2e2; color: #991b1b"] * len(row)
        elif valor == "DISPONIBLE":
            return ["background-color: #d1fae5; color: #065f46"] * len(row)
    return [""] * len(row)

# ============================================================
# 5. CABECERA
# ============================================================
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image(
        "https://ugelcusco.gob.pe/ws/wp-content/uploads/2026/02/LOGOOOO.fw_.png",
        width=140
    )
with col_titulo:
    st.subheader("UNIDAD DE GESTIÓN EDUCATIVA LOCAL CUSCO")
    st.title("ADJUDICACIÓN DE PLAZAS CONTRATO DOCENTE")
    st.markdown(
        "<span class='status-live'>● ACTUALIZACIÓN EN VIVO (CADA 15s)</span>",
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# 6. URL DE LA HOJA DE CÁLCULO
# ============================================================
URL_SHEET = (
    "https://docs.google.com/spreadsheets/d/"
    "1X78ctrqUH58bpjj57ibWucgpGrrw4NAG/edit?usp=sharing"
)

# ============================================================
# 7. CARGA, FILTROS Y TABLA
# ============================================================
try:
    df_original = cargar_datos(URL_SHEET)
    df = df_original.copy()

    # --- CONTADORES RESUMEN ---
    col_estado_global = next(
        (c for c in df.columns if "ESTADO" in c.upper()), None
    )
    if col_estado_global:
        total = len(df)
        disponibles = (df[col_estado_global].str.strip().str.upper() == "DISPONIBLE").sum()
        adjudicadas = (df[col_estado_global].str.strip().str.upper() == "ADJUDICADA").sum()

        m1, m2, m3 = st.columns(3)
        m1.metric("📋 Total de Plazas", total)
        m2.metric("✅ Disponibles", disponibles, delta=None)
        m3.metric("🔴 Adjudicadas", adjudicadas, delta=None)
        st.divider()

    # --- FILTROS ---
    st.write("### 🔍 Búsqueda Avanzada")
    c1, c2, c3 = st.columns(3)

    with c1:
        col_nivel = next((c for c in df.columns if "NIVEL" in c.upper()), None)
        if col_nivel:
            lista_niveles = ["TODOS"] + sorted(df[col_nivel].dropna().unique().tolist())
            nivel_sel = st.selectbox("Nivel Educativo:", lista_niveles)
            if nivel_sel != "TODOS":
                df = df[df[col_nivel] == nivel_sel]
        else:
            st.warning("Columna 'NIVEL' no encontrada")

    with c2:
        col_cargo = next((c for c in df.columns if "CARGO" in c.upper()), None)
        if col_cargo:
            lista_cargos = ["TODOS"] + sorted(df[col_cargo].dropna().unique().tolist())
            cargo_sel = st.selectbox("Cargo:", lista_cargos)
            if cargo_sel != "TODOS":
                df = df[df[col_cargo] == cargo_sel]
        else:
            st.warning("Columna 'CARGO' no encontrada")

    with c3:
        busqueda = st.text_input(
            "Búsqueda por IE y/o Especialidad:",
            placeholder="Escriba aquí..."
        )
        if busqueda:
            mask = df.astype(str).apply(
                lambda x: x.str.contains(busqueda, case=False, na=False)
            ).any(axis=1)
            df = df[mask]

    # --- TABLA CON ESTILOS ---
    if not df.empty:
        styled_df = df.style.apply(estilo_fila, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=550, hide_index=True)
        st.caption(f"Mostrando {len(df)} de {len(df_original)} plazas")
    else:
        st.info("No se encontraron plazas con los filtros seleccionados.")

except Exception as e:
    st.error(f"❌ Error en la sincronización: {e}")
    st.info(
        "Verifica que el archivo de Google Sheets sea público "
        "(Archivo → Compartir → Cualquier persona con el enlace puede ver)"
    )

# ============================================================
# 8. PIE DE PÁGINA
# ============================================================
st.markdown(
    '<div class="footer">'
    "© 2026 Equipo de Informática - UGEL Cusco<br/>"
    "Este tablero es meramente informativo.<br/>"
    "La adjudicación oficial se realiza en acto público."
    "</div>",
    unsafe_allow_html=True
)
