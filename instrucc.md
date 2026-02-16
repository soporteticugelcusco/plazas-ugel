**3. Cómo publicarlo (Gratis y para 2,000 personas)**

**Para que los usuarios puedan entrar desde su celular o PC:**



**Sube tu código a GitHub: Crea un repositorio privado o público con el archivo app.py y un archivo llamado requirements.txt que solo diga:**



**Plaintext**

**streamlit**

**pandas**

**Conecta con Streamlit Cloud:**



**Ve a share.streamlit.io.**   https://share.streamlit.io/



**Conecta tu cuenta de GitHub.**



**Selecciona tu repositorio y dale a "Deploy".**



**¡Listo! Te dará un link tipo https://tu-app-plazas.streamlit.app/ que es el que compartirás con las 2,000 personas.**

----



Para lograr una actualización casi instantánea para 2,000 personas sin colapsar el sistema, vamos a usar una combinación de Google Sheets (como base de datos por su velocidad), GitHub (para guardar el código) y Streamlit Cloud (para el hosting gratuito).



Aquí tienes la guía paso a paso desde cero:



Paso 1: Preparar la Base de Datos (Google Sheets)

Aunque el dueño use Excel, lo más eficiente es que el archivo viva en Google Sheets para que Python lo lea por URL sin bloqueos.



Sube tu Excel a Google Sheets.



Asegúrate de que la primera fila tenga los nombres de las columnas (ej: ID, Plaza, Estado, Postulante).



Haz clic en Compartir > Cualquier persona con el enlace > Lector.



Copia el enlace de compartir.



Paso 2: Crear el Código en Python (app.py)

He modificado el código para que la actualización sea de 3 segundos. También añadí un fragmento de código que hace que la página se "auto-refresque" visualmente.



Crea un archivo llamado app.py en tu computadora y pega esto:



Python

import streamlit as st

import pandas as pd

import time



\# Configuración de página

st.set\_page\_config(page\_title="Adjudicación de Plazas en Vivo", layout="wide")



\# Estilo para que se vea profesional

st.markdown("""

&nbsp;   <style>

&nbsp;   .stApp { background-color: #f5f7f9; }

&nbsp;   .status-viva { color: #28a745; font-weight: bold; }

&nbsp;   </style>

&nbsp;   """, unsafe\_allow\_html=True)



st.title("📋 Seguimiento de Adjudicación de Plazas")

st.markdown(f"\*\*Estado:\*\* <span class='status-viva'>● EN VIVO</span>", unsafe\_allow\_html=True)



\# --- CONFIGURACIÓN DE LA BASE ---

\# Reemplaza con tu link de Google Sheets

URL\_SHEET = "TU\_LINK\_DE\_GOOGLE\_SHEETS\_AQUÍ"



\# --- CARGA DE DATOS CON CACHÉ DE 3 SEGUNDOS ---

@st.cache\_data(ttl=3)

def cargar\_plazas(url):

&nbsp;   # Transformamos el link para descarga directa en CSV

&nbsp;   csv\_url = url.replace('/edit?usp=sharing', '/export?format=csv')

&nbsp;   return pd.read\_csv(csv\_url)



try:

&nbsp;   df = cargar\_plazas(URL\_SHEET)



&nbsp;   # Buscador rápido

&nbsp;   busqueda = st.text\_input("🔍 Buscar plaza, institución o estado:", placeholder="Escribe aquí...")



&nbsp;   if busqueda:

&nbsp;       df = df\[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]



&nbsp;   # Mostrar la tabla

&nbsp;   st.dataframe(df, use\_container\_width=True, height=500)



&nbsp;   # --- AUTO-REFRESCO VISUAL ---

&nbsp;   # Esto obliga al navegador a pedir datos nuevos cada 3 segundos

&nbsp;   time.sleep(3)

&nbsp;   st.rerun()



except Exception as e:

&nbsp;   st.error("Conectando con el servidor de datos...")

&nbsp;   time.sleep(2)

&nbsp;   st.rerun()

Paso 3: Crear el archivo de dependencias (requirements.txt)

Crea otro archivo en la misma carpeta llamado requirements.txt con este contenido:



Plaintext

streamlit

pandas

Paso 4: Subir a GitHub

Entra a GitHub y crea un repositorio nuevo (ej: plazas-ugel).



Sube tus dos archivos: app.py y requirements.txt.



Paso 5: Desplegar en Streamlit Cloud (El Hosting)

Ve a share.streamlit.io.



Conéctate con tu cuenta de GitHub.



**Haz clic en "New app".**



**Selecciona tu repositorio, la rama (main) y el archivo (app.py).**



**Haz clic en "Deploy!".**



Por qué esto funcionará para tus 2,000 usuarios:

Actualización de 3 segundos: El comando @st.cache\_data(ttl=3) le dice a Python: "No leas el archivo de Google cada vez que alguien entre; lee el archivo una vez, guárdalo en memoria 3 segundos, y dáselo a todos los que pregunten".



Sin colapsos: Google Sheets soporta que Python pida el CSV cada 3 segundos sin problemas.



Auto-actualización: El comando st.rerun() al final del código hace que la página de los 2,000 usuarios se refresque sola cada 3 segundos, así ellos no tienen que presionar nada para ver si una plaza ya se ocupó.



¿Tienes ya el link de Google Sheets para probar si el código lee los datos correctamente? Solo recuerda cambiar la parte de URL\_SHEET en el código.





---------------






