import streamlit as st
from pathlib import Path
import sys
from PIL import Image

cwd = Path('.').resolve()
sys.path.append(str(cwd))

from paths import SOLCI_ARROYO_PROFILE_PATH, CHECHU_MARFIA_PROFILE_PATH, AGUS_OLIA_PROFILE_PATH, LOGO_PATH  # noqa

st.set_page_config(page_title='Inicio PyTrivia ⏳')

col1, col2, col3 = st.columns(3)

with col2:
    img = Image.open(LOGO_PATH)
    st.image(img, use_column_width=True)


def pagina_inicio():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>¡Bienvenidx a PyTrivia 👋🏼!</h1>
            <p>👥 Somos el grupo 22</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        img = Image.open(SOLCI_ARROYO_PROFILE_PATH)
        st.image(img,
                 caption='👩🏻‍💻 SOL JUSTINA ARROYO TABARI', use_column_width=True)

    with col2:
        img = Image.open(CHECHU_MARFIA_PROFILE_PATH)
        st.image(img,
                 caption='👩🏻‍💻 CECILIA MARFIA', use_column_width=True)

    with col3:
        img = Image.open(AGUS_OLIA_PROFILE_PATH)
        st.image(img,
                 caption='👩🏻‍💻 MARÍA AGUSTINA OLIA', use_column_width=True)


pagina_inicio()
st.markdown("---")
st.header("📋 Descripción del juego PyTrivia")
st.markdown("""🕹️ PyTrivia es un juego de preguntas y respuestas diseñado sobre aeropuertos, lagos, conectividad y censo 2022 para la cátedra de
            Seminario de lenguaje: Python🐍 donde podrás poner a prueba tus conocimientos en diferentes temáticas de datos de Argentina 🇦🇷
            vas a poder desafiar tu mente 🧠 y aprender algo nuevo cada vez que juegues ⚡️! """)
st.markdown("---")
st.header("🧚♀️ Instrucciones básicas para jugar")

st.markdown("""
1. **Registro**
   - Selecciona tu nombre de usuarix, si es que ya estás registradx, sino vas a poder acceder al""")
st.page_link("pages/04_Formulario_de_registro.py",
             label=" Formulario de registro 📝")
st.markdown("""   - Elige la dificultad y la temática de las preguntas.

2. **Inicio del juego 😵💫**
   - Una vez configurados los datos, presiona el botón "Jugar" para comenzar.
   - Se te presentarán preguntas según la temática seleccionada.

3. **Responder preguntas 🤓**
   - Lee atentamente cada pregunta.
   - Selecciona o ingresa la respuesta según la dificultad elegida:
     - 🟢 **Fácil:** Selecciona una respuesta de las opciones dadas.
     - 🟡 **Media:** Se te dará una pista (número de palabras) y deberás escribir la respuesta.
     - 🔴 **Alta:** Deberás escribir la respuesta sin pistas.

4. **Puntuación 🏆**
   - Responde tantas preguntas como puedas.
   - Al finalizar, se te mostrará tu puntaje y las respuestas correctas.

5. **Estadísticas 📈**
    - Podés ir a la sección de estadísticas para ver los distintos gráficos y datos que relevamos de las partidas.
""")

st.markdown("---")

st.header("📌 Menú de enlaces")

# st.page_link("pages/01_Inicio.py", label="🏁 Inicio")
st.page_link("pages/02_Conociendo_nuestros_datos.py",
             label="🔍 Conociendo nuestros datos")
st.page_link("pages/03_Juego.py", label="🧩 Juego")
st.page_link("pages/04_Formulario_de_registro.py",
             label="📋 Formulario de registro")
st.page_link("pages/05_Ranking.py", label="🏅 Ranking")
st.page_link("pages/06_Seccion_de_estadisticas.py",
             label="📊 Sección de estadísticas")
