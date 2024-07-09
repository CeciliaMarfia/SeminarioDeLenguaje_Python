from pathlib import Path
import streamlit as st
import random
import json
import sys
import datetime
import pandas as pd
import os

st.set_page_config(page_title='Página de Juego 🎮')

cwd = Path('.').resolve()
sys.path.append(str(cwd))

from paths import USER_DB_PATH  # noqa
from paths import MATCH_DB_PATH  # noqa

try:
    with open(USER_DB_PATH, 'r') as file:
        usuarios_data = json.load(file)
except FileNotFoundError:
    st.markdown(
        "### ⏳ Aún no hay usuarios disponibles. ¡Registrate para empezar a jugar! 👾")
    st.page_link("pages/04_Formulario_de_registro.py",
                 label="Formulario de registro", icon="👥")
    # Deja de ejecutar el resto del archivo
    st.stop()

users_names = [
    f"{value['username']} ({key})" for key, value in usuarios_data.items()]

difficulty_options = ["🟢 Fácil: Se le brindan respuestas de las cuales una es la correcta.",
                      "🟡 Media: Se le informa la cantidad de palabras de la respuesta.", "🔴 Alta: No se brindan ayudas."]
theme_options = {"✈️ Aeropuertos": 'ar-airports_copy.csv',
                 "🏞️ Lagos": 'lagos_arg_copy.csv',
                 "📡 Conectividad": 'Conectividad_Internet_copy.csv',
                 "👥 Censos 2022": 'c2022_tp_c_resumen_adaptado_copy.csv'}

columns_by_theme = {"✈️ Aeropuertos": {
    'original': ['ident', 'type', 'name', 'elevation_ft', 'country_name', 'municipality', 'elevation_name', 'prov_name'],
    'new': ['Identificador', 'Tipo', 'Nombre', 'Elevación (ft)', 'Nombre del País', 'Municipio', 'Elevación', 'Nombre de la Provincia']
},
    "🏞️ Lagos": {
    'original': ['Nombre', 'Ubicación', 'Superficie (km²)', 'Profundidad máxima (m)', 'Profundidad media (m)', 'Sup Tamaño'],
    'new': ['Nombre', 'Ubicación', 'Superficie (km²)', 'Profundidad máxima (m)', 'Profundidad media (m)', 'Tamaño de superficie']
},
    "📡 Conectividad": {
    'original': ['Provincia', 'Localidad', 'Poblacion', 'ADSL', 'CABLEMODEM', 'DIALUP', 'FIBRAOPTICA', 'SATELITAL', 'WIRELESS', 'TELEFONIAFIJA', '3G', '4G', 'posee_conectividad'],
    'new': ['Provincia', 'Localidad', 'Poblacion', '¿Posee ADSL?', '¿Posee CABLEMODEM?', '¿Posee DIALUP?', '¿Posee FIBRAOPTICA?', '¿Posee SATELITAL?', '¿Posee WIRELESS?', '¿Posee TELEFONIA FIJA?', '¿Posee 3G?', '¿Posee 4G?', '¿Posee Conectividad?']
},
    "👥 Censos 2022": {
    'original': ['Jurisdicción', 'Total de población', 'Población en viviendas particulares', 'Población en viviendas colectivas (¹)', 'Población en situación de calle(²)', 'Varones Total de población', 'VaronesPoblación en situación de calle(²)', 'Mujeres Total de población', 'Mujeres Población en situación de calle(²)'],
    'new': ['Jurisdicción', 'Total de población', 'Población en viviendas particulares', 'Población en viviendas colectivas', 'Población en situación de calle', 'Varones Total de población', 'Varones Población en situación de calle', 'Mujeres Total de población', 'Mujeres Población en situación de calle']
}
}


def game_page():
    st.title('¡Bienvenidxs a PyTrivia! 🎮')
    st.write('¡Regístrese para comenzar a jugar 😊!')


def questions_page():
    st.title(' Comenzando la Pytrivia 🎮')


def end_of_game():
    # Muestra el resumen de resultados al finalizar el juego.
    st.title('¡Has respondido todas las preguntas! 🎉')
    st.session_state.show_ranking = True
    st.page_link("pages/05_Ranking.py",
                 label="Ver puntaje", icon="🏁")
    st.write("---")
    answers = st.session_state.game_state["answers"]
    for question_number, answers in answers.items():
        st.write(f"🔹 <u>Pregunta {question_number}</u>:",
                 unsafe_allow_html=True)
        st.write(f"👤 Respuesta del usuario: {answers['user_answer']}")
        st.write(f"🤓 Respuesta esperada: {answers['correct_answer']}")
        if str(answers['user_answer']).strip().lower() == str(answers['correct_answer']).strip().lower():
            st.write("<b><font color='green'>✅ ¡Correcto!</font></b>",
                     unsafe_allow_html=True)
        else:
            st.write("<b><font color='red'>❌ ¡Incorrecto!</font></b>",
                     unsafe_allow_html=True)
        st.write("---")


def generate_question(df, difficulty):
    # Selecciona una fila aleatoria del dataframe
    row = df.sample().iloc[0]

    # Selecciona cuatro columnas aleatorias de la fila
    columns = random.sample(list(df.columns), 4)

    # Construye la pregunta y las opciones
    question = {col: row[col] for col in columns[:-1]}
    correct_answer = row[columns[-1]]

    options = []
    if difficulty[0] == '🟢':
        unique_answers = list(df[columns[-1]].unique())
        options = random.sample(unique_answers, min(3, len(unique_answers)))
        if correct_answer not in options:
            options[random.randint(0, len(options) - 1)] = correct_answer
        random.shuffle(options)
    return question, correct_answer, columns[-1], options


def difficulty_scoring(difficulty, score):
    # Calcula el puntaje según la dificultad de una pregunta
    difficulty = difficulty[0]
    if difficulty == '🟡':
        score = score*1.5
    elif difficulty == '🔴':
        score = score * 2
    return score


def normalize_text(text):
    # Normaliza un texto convirtiéndolo a minúsculas y eliminando espacios al inicio y final
    return str(text).strip().lower()


# Si no existe el estado, lo creo
original_state = {
    "state": "NO_CREADO",
    "user": "",
    "correct_answers": 0,
    "last_answer": "",
    "last_question": "",
    "last_hidden_attribute": "",
    "last_correct_answer": "",
    "questions_generated": 0,
    "start_time": None,
    "end_time": None,
    "difficulty": "",
    "theme": "",
    "answers": {}
}
if "game_state" not in st.session_state:
    st.session_state["game_state"] = original_state

df = None

if st.session_state.game_state["state"] == "NO_CREADO":
    game_page()
    with st.form("user_selection"):
        user = st.selectbox(
            "👤 Selecciona tu nombre de usuarix",
            options=users_names + ["Otrx"],
            index=None,
            placeholder="",
        )
        difficulty = st.selectbox("🌡️ Selecciona la dificultad",
                                  options=difficulty_options,
                                  # index=None,
                                  placeholder="",
                                  )
        theme = st.selectbox("🗺️ Selecciona la temática",
                             options=theme_options.keys(),
                             # index=None,
                             placeholder="",
                             )
        jugar = st.form_submit_button("Jugar")
        if jugar:
            if user == "Otrx":
                st.write("Para jugar debes estar registradx, en:")
                st.page_link("pages/04_Formulario_de_registro.py",
                             label="Formulario de registro", icon="👥")
            elif user == None:
                st.warning('⚠️ Debe seleccionar unx usuarix.')
            else:
                st.session_state.game_state["start_time"] = datetime.datetime.now(
                )
                st.session_state.game_state['difficulty'] = difficulty
                st.session_state.game_state['theme'] = theme
                st.session_state.game_state["state"] = "GENERAR_PREGUNTA"
                st.session_state.game_state["user"] = user
                st.rerun()

elif st.session_state.game_state["state"] == "GENERAR_PREGUNTA":
    st.session_state.game_state["state"] = "NUEVO"
    # Se debe cargar siempre que se genera una pregunta porque al hacer
    # st.rerun() en el estado NO_CREADO se pierden las variables
    df = pd.read_csv(
        Path('datasets/processed_datasets')/theme_options[st.session_state.game_state['theme']])
    columns = columns_by_theme[st.session_state.game_state['theme']]['original']
    df = df[columns]
    # Renombra las columnas
    new_columns = columns_by_theme[st.session_state.game_state['theme']]['new']
    df.columns = new_columns

    df.dropna(inplace=True)

    if st.session_state.game_state["difficulty"][0] == '🟢':
        while True:
            question, correct_answer, hidden_attribute, options = generate_question(
                df, st.session_state.game_state['difficulty'])
            if len(options) > 1:
                break
    else:
        question, correct_answer, hidden_attribute, options = generate_question(
            df, st.session_state.game_state['difficulty'])

    print("\033[91mquestion\033[0m", question,
          "\033[92mcorrect_answer\033[0m", correct_answer,
          "\033[94mhidden_attribute\033[0m", hidden_attribute,
          "\033[33moptions\033[0m", options)

    st.session_state.game_state["last_question"] = question
    st.session_state.game_state["last_hidden_attribute"] = hidden_attribute
    st.session_state.game_state["last_correct_answer"] = correct_answer
    st.session_state.game_state["last_options"] = options

    st.rerun()

elif st.session_state.game_state["state"] == "NUEVO":
    with st.form("questions"):
        question = st.session_state.game_state["last_question"]
        hidden_attribute = st.session_state.game_state["last_hidden_attribute"]
        correct_answer = st.session_state.game_state["last_correct_answer"]
        options = st.session_state.game_state["last_options"]

        st.write("**🔍 Pregunta:**")
        for key, value in question.items():
            st.write(f"**🔸{key}:** {value}")

        if st.session_state.game_state['difficulty'][0] == '🟢':
            respuesta = st.radio(f"**🔹{hidden_attribute}:** ", options)
        elif st.session_state.game_state['difficulty'][0] == '🟡':
            st.write(
                f"**👀 Pista:** La respuesta tiene {len(str(correct_answer).split())} palabra/s.")
            st.write(f"**🔹{hidden_attribute}:** ")
            respuesta = st.text_input("Respuesta", "")
        else:
            st.write(f"**🔹{hidden_attribute}:** ")
            respuesta = st.text_input("Respuesta", "")
        responder = st.form_submit_button("Responder")

    if responder:
        st.session_state.game_state['questions_generated'] += 1
        if normalize_text(respuesta) == normalize_text(correct_answer):
            st.session_state.game_state["correct_answers"] += 1
        st.session_state.game_state["last_answer"] = respuesta

        questions_generated = st.session_state.game_state["questions_generated"]
        answers = st.session_state.game_state["answers"]
        answers[str(questions_generated)] = {
            "user_answer": respuesta,
            "correct_answer": correct_answer
        }
        st.session_state.game_state["answers"] = answers

        if st.session_state.game_state['questions_generated'] == 5:  # fin del juego
            st.session_state.game_state["end_time"] = datetime.datetime.now()
            st.session_state.game_state["state"] = "MOSTRAR_PUNTAJE"
            st.rerun()
        else:
            st.session_state.game_state["state"] = "GENERAR_PREGUNTA"
            st.rerun()

elif st.session_state.game_state["state"] == "MOSTRAR_PUNTAJE":
    session = {'fecha_y_hora_inicio': st.session_state.game_state["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
               'fecha_y_hora_fin': st.session_state.game_state["end_time"].strftime("%Y-%m-%d %H:%M:%S"),
               'usuario': st.session_state.game_state['user'],
               'dificultad': st.session_state.game_state['difficulty'],
               'tematica': st.session_state.game_state['theme'],
               'respuestas_correctas': st.session_state.game_state["correct_answers"],
               'puntaje': difficulty_scoring(st.session_state.game_state['difficulty'], st.session_state.game_state['correct_answers'])
               }
    # La siguiente línea de código verifica si no existe un archivo o directorio en la ruta declarada
    if not os.path.exists(MATCH_DB_PATH):
        with open(MATCH_DB_PATH, 'w') as file:
            json.dump([], file)
    with open(MATCH_DB_PATH, 'r') as file:
        matches = json.load(file)
    matches.append(session)
    with open(MATCH_DB_PATH, 'w') as file:
        json.dump(matches, file, indent=2)
    end_of_game()
    # Permite reiniciar juego
    st.session_state["game_state"] = original_state
