from paths import MATCH_DB_PATH
from paths import KUN_AGUERO_MEME_PATH
import streamlit as st
import pandas as pd


st.set_page_config(page_title='Ranking 🏅')


def game_results():
    st.markdown("# 🎮 Resultados de la Partida")
    st.markdown("---")


def add_positions(file):
    try:
        # Ordena por puntaje para asignarle el puesto
        df_sessions = file.sort_values(by=['puntaje'], ascending=False)
        df_sessions['puesto'] = range(1, len(df_sessions) + 1)
        return df_sessions
    except Exception as e:
        raise


def position_message(position):
    if position == 1:
        st.success("🏆¡Felicidades! ¡Eres el primer lugar!")
    elif position == 2:
        st.success("🥈¡Genial! ¡Estás en el segundo lugar!")
    elif position == 3:
        st.success("🥉¡Muy bien! ¡Estás en el tercer lugar!")
    elif position > 3:
        st.success(
            f"🎖️ Estás en la posición {position}. ¡Sigue esforzándote para subir en el ranking!")


try:
    file = pd.read_json(MATCH_DB_PATH)
    game_sessions = add_positions(file)

    if st.session_state.get("show_ranking"):
        game_results()

        # Ordena el dataframe por fecha para acceder a la última partida
        game_sessions = game_sessions.sort_values(
            by=['fecha_y_hora_fin'], ascending=True)

        # Preguntas de la partida en conjunto con la respuesta correcta y la respuesta del usuario.
        last_game = game_sessions.iloc[-1]
        correct_answers = last_game["respuestas_correctas"]
        st.text(f"✅ Cantidad de respuestas correctas: {correct_answers}")
        score = last_game["puntaje"]
        st.text(f"🎯 Puntaje de la partida: {score}")
        ranking_position = last_game["puesto"]
        position_message(ranking_position)

    st.markdown("# 🏆 Ranking Histórico")
    st.markdown("---")

    # Ordena el dataframe por puesto
    game_sessions_sorted = game_sessions.sort_values(
        by='puesto', ascending=True)

    top_15 = game_sessions_sorted.head(15)
    # top_15.columns = map(str.upper, top_15.columns)
    top_15['puesto'] = top_15['puesto'].astype(str)
    top_15['puesto'] = top_15['puesto'].apply(lambda x: "1 🥇" if x == '1' else (
        "2 🥈" if x == '2' else ("3 🥉" if x == '3' else x)))
    top_15.set_index('puesto', inplace=True)
    top_15['puntaje'] = '🪙 ' + top_15['puntaje'].round(2).astype(str)
    top_15_display = top_15[['usuario', 'puntaje']]
    data_to_show = top_15.reset_index().values.tolist()

    table_style = """
        <style>
            table {
                color: #F0F0F0; /* Blanco suave */
                background-color: #2C3E50; /* Azul oscuro */
                border-collapse: collapse;
                width: 100%;
                font-family: 'Arial', sans-serif; /* Fuente más limpia */
            }
            th {
                background-color: #34495E; /* Azul intermedio */
                border: 1px solid #ECF0F1; /* Blanco claro */
                padding: 10px;
                text-align: left;
            }
            td {
                border: 1px solid #ECF0F1; /* Blanco claro */
                padding: 10px;
                text-align: left;
            }
            tr:nth-child(odd) {
                background-color: #3B5998; /* Azul intermedio */
            }
            tr:nth-child(even) {
                background-color: #2C3E50; /* Azul oscuro */
            }
            tr:hover {
                background-color: #1ABC9C; /* Verde menta */
            }
        </style>
    """
    top_15_display.columns = top_15_display.columns.str.capitalize()
    st.write(table_style, unsafe_allow_html=True)
    st.table(top_15_display)

except:
    st.markdown(
        "### ⏳ Aún no hay partidas disponibles. ¡Empieza a jugar para registrar tus partidas! 👾")
    KUN_AGUERO_MEME_PATH = str(KUN_AGUERO_MEME_PATH)
    st.image(KUN_AGUERO_MEME_PATH, use_column_width=True)

    # Define el botón utilizando HTML
    button_style = '''
    background-color: #4CAF50;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 20px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 12px;
'''
    # Crea el enlace HTML para el botón
    page = 'Juego'
    button_html = f'<a href="{page}" target="_self" style="{button_style}">Ir a juga 🎮</a>'

    # Muestra el botón utilizando st.markdown
    st.markdown(button_html, unsafe_allow_html=True)
