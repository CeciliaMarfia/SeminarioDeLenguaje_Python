from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import json
import sys
from collections import defaultdict
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title='Sección de estadísticas 📊')

cwd = Path('.').resolve()
sys.path.append(str(cwd))

from paths import USER_DB_PATH  # noqa
from paths import MATCH_DB_PATH  # noqa

# Intenta abrir el archivo de usuarios
try:
    with open(USER_DB_PATH, 'r') as file:
        usuarios_data = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    st.markdown(
        "### ⏳ Aún no hay usuarios disponibles. ¡Registrate para empezar a jugar! 👾")
    st.page_link("pages/04_Formulario_de_registro.py",
                 label="Formulario de registro", icon="👥")
    st.stop()  # Deja de ejecutar el resto del código

# Intenta abrir el archivo de partidas
try:
    with open(MATCH_DB_PATH, 'r') as file:
        matches = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    st.markdown(
        "### ⏳ Aún no hay partidas disponibles. ¡Empieza a jugar para registrar tus partidas! 👾")
    st.page_link("pages/03_Juego.py", label="¡Comienza a jugar!", icon="🧩")
    st.stop()  # Deja de ejecutar el resto del código


color_mapping = {
    'Femenino': '#FF69B4',
    'Masculino': '#87CEFA',
    'Otro': '#E6E6FA',
    'Prefiero no decirlo': '#FAFAD2'
}
st.markdown("""
<style>
.bold-text {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


def bold_text(text):
    return f'<span class="bold-text">{text}</span>'


def statistics_page():
    st.title('Sección de estadísticas 📊')


statistics_page()

css = """
    <style>
    table {
        width: 80%;
        margin-left: auto;
        margin-right: auto;
        text-align: center;  /* Alinea el texto de las celdas al centro */
    }
    th, td {
        padding: 8px;  /* Espaciado interno de las celdas */
    }
    th {
        text-align: center; /* Centra el texto del encabezado */
    }
    </style>
    """
st.markdown(css, unsafe_allow_html=True)

######################################################

usuarios_data_keys = list(usuarios_data.keys())
usuarios_jugaron = {entry['usuario'].split('(')[1][:-1] for entry in matches}

# Genera la lista de booleanos
usuarios_jugaron_lista = [
    email in usuarios_jugaron for email in usuarios_data_keys]

# Ejemplo de datos de usuarios
data = {
    'user_id': usuarios_data_keys,
    'gender': [v["gender"] for k, v in usuarios_data.items()],
    'has_played': usuarios_jugaron_lista
}

# Convierte a DataFrame
users_df = pd.DataFrame(data)

# Filtra usuarios que hayan jugado alguna vez
played_users_df = users_df[users_df['has_played'] == True]

# Cuenta la cantidad de usuarios por género
gender_counts = played_users_df['gender'].value_counts()


# Configuración de Streamlit
st.title("Estadísticas de Uso del Juego")
st.markdown("---")
# subtitulo
text = "Usuarixs que hayan jugado alguna vez el juego agrupados por género 🙌🏼"
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

# Gráfico de torta
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index,
       autopct='%1.1f%%', startangle=90, colors=[color_mapping[key] for key in gender_counts.index])
ax.axis('equal')  # Para que el gráfico sea un círculo

# Muestra gráfico en Streamlit
st.pyplot(fig)

# Muestra los datos en una tabla
st.write("Datos de usuarios que han jugado alguna vez:")
# st.dataframe(played_users_df)
new_names = {'user_id': 'Usuario', 'gender': 'Género', 'has_played': '¿Jugó?'}
played_users_df = played_users_df.rename(columns=new_names)
table_html = played_users_df.reset_index(drop=True).to_html(index=False)
st.markdown(table_html, unsafe_allow_html=True)

######################################################

# 2. Gráfico de torta para partidas con puntuación superior a la media

st.markdown("---")

text = "Porcentaje de partidas con puntuación superior a la media 🎯"
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

# Obtiene todas las puntuaciones de las partidas
scores = [partida["respuestas_correctas"] for partida in matches]

# Calcula la puntuación media
average_score = sum(scores) / len(scores)

# Cuenta partidas superiores e inferiores a la media
above_average_count = sum(1 for score in scores if score > average_score)
below_average_count = len(scores) - above_average_count

# Datos para el gráfico de torta
labels = ['Sobre la media', 'Bajo la media']
sizes = [above_average_count, below_average_count]
colors = ['#FF9999', '#66B2FF']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.axis('equal')  # Para que el gráfico sea un círculo

# Muestra el gráfico en Streamlit
st.pyplot(fig)

######################################################

# 3. Gráfico de barras para que cada día de la semana muestre la cantidad de partidas realizadas

days_translation = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
days_order = ['Lunes', 'Martes', 'Miércoles',
              'Jueves', 'Viernes', 'Sábado', 'Domingo']


def get_day(date):
    return date.strftime('%A')


st.markdown("---")

text = "Cantidad de partidas realizadas por día de la semana 🗓️ "
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

df = pd.DataFrame(matches)

df['fecha_y_hora_inicio'] = pd.to_datetime(
    df['fecha_y_hora_inicio'], format='%Y-%m-%d %H:%M:%S')

# Obtiene los días
df['dia_semana'] = df['fecha_y_hora_inicio'].apply(
    get_day).map(days_translation)

# Obtiene la cantidad de partidas por día
games_per_day = df['dia_semana'].value_counts().reindex(
    days_order, fill_value=0)

# Crea el gráfico
fig, ax = plt.subplots()
games_per_day.plot(kind='bar', ax=ax, color=[
                   'pink', 'purple', 'skyblue', 'green'])
ax.set_xlabel('Día de la semana')
ax.set_ylabel('Cantidad de partidas')

# Muestra el gráfico en Streamlit
st.pyplot(fig)


######################################################
# 4. Promedio de respuestas acertadas mensuales  e/ un rango de dos fechas insertadas en dos unputs

st.markdown("---")
text = "⭐️ Promedio de preguntas acertadas mensuales entre el rango de fechas seleccionado:"
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

df_matches = pd.DataFrame(matches)

# Claves para identificar cada campo de entrada
key_start_date = 'start_e4'
key_end_date = 'end_e4'

# Entrada de fechas
start_date = st.date_input(
    "Fecha de inicio", value=datetime(2024, 1, 1), key=key_start_date)
end_date = st.date_input(
    "Fecha de fin", value=datetime.now(), key=key_end_date)

# Convierte start_date y end_date en datatime combinando la fecha con una hora específica
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# Filtra los datos en base a las fechas seleccionadas
filtered_matches = [
    match for match in df_matches.itertuples(index=False)
    if start_datetime <= datetime.strptime(match.fecha_y_hora_inicio, '%Y-%m-%d %H:%M:%S') <= end_datetime
]

monthly_correct_answers = defaultdict(list)

for match in filtered_matches:
    # Utiliza el formato correcto para incluir la hora, minutos y segundos
    month = datetime.strptime(
        match.fecha_y_hora_inicio, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
    monthly_correct_answers[month].append(match.respuestas_correctas)

monthly_average_correct_answers = {
    month: sum(scores) / len(scores)
    for month, scores in monthly_correct_answers.items()
}

# Convierte a DataFrame
df_monthly_average = pd.DataFrame(list(monthly_average_correct_answers.items()), columns=[
                                  'Mes', 'Promedio de Respuestas Correctas'])
df_monthly_average = df_monthly_average.sort_values(by='Mes')

# Convierte la columna 'Promedio de Respuestas Correctas' a numérica si es necesario
df_monthly_average['Promedio de Respuestas Correctas'] = pd.to_numeric(
    df_monthly_average['Promedio de Respuestas Correctas'])
if not df_monthly_average.empty:

    # Grafica
    fig, ax = plt.subplots()
    df_monthly_average.plot(kind='bar', x='Mes', y='Promedio de Respuestas Correctas', ax=ax, color=[
                            'pink', 'purple', 'skyblue', 'green'])
    plt.xticks(rotation=45)
    plt.ylabel('Promedio de Respuestas Correctas')
    st.pyplot(fig)
else:
    st.write("⛔️ No hay datos disponibles para las fechas seleccionadas.")

######################################################

# 5. Top 10 usuarios con mayor cantidad de puntos acumulados entre un rango de dos fechas insertadas por input.

st.markdown("---")
text = "⭐️ Top 10 usuarios con mayor cantidad de puntos entre el rango de fechas seleccionado: "
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

df = pd.DataFrame(matches)

# Claves para identificar cada campo de entrada
key_start_date = 'start_e5'
key_end_date = 'end_e5'

# Inicializa las entradas en la fecha actual
start_date = st.date_input(
    "Fecha de inicio", value=datetime(2024, 1, 1), key=key_start_date)
end_date = st.date_input(
    "Fecha de fin", value=datetime.now(), key=key_end_date)

# Convierte start_date y end_date en datatime combinando la fecha con una hora específica
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

df['fecha_y_hora_inicio'] = pd.to_datetime(df['fecha_y_hora_inicio'])

filtered_df = df[(df['fecha_y_hora_inicio'] >= start_datetime)
                 & (df['fecha_y_hora_inicio'] <= end_datetime)]
if not filtered_df.empty:
    accumulated_scores = filtered_df.groupby(
        'usuario')['puntaje'].sum().reset_index()
    top_10 = accumulated_scores.sort_values(
        by='puntaje', ascending=False).head(10)

    top_10.columns = top_10.columns.str.capitalize()

    # Muestra la tabla centrada horizontalmente
    table_html = top_10.to_html(index=False)

    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.write("⛔️ No hay datos disponibles para las fechas seleccionadas.")

######################################################

# 6. Ordenar los datasets por dificultad donde primero se debe ubicar el dataset que tiene mayor numero de errores en las respuestas

st.markdown("---")
text = "📎 Datasets ordenados por dificultad de mayor a menor según la cantidad de errores en las respuestas."
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

df = pd.DataFrame(matches)

# Calcula la cantidad de respuestas incorrectas
df['respuestas_incorrectas'] = 5 - df['respuestas_correctas']

# Calcula el promedio de respuestas incorrectas por tema. Devuelve un nuevo dataframe con indices numéricos simples
avg_responses = df.groupby('tematica')[
    'respuestas_incorrectas'].mean().reset_index()
avg_responses.columns = ['Temática', 'Promedio de respuestas incorrectas']

# Ordena por promedio de respuestas incorrectas (descendente)
avg_responses = avg_responses.sort_values(
    by='Promedio de respuestas incorrectas', ascending=False).reset_index(drop=True)

avg_responses.columns = avg_responses.columns.str.capitalize()

table_html = avg_responses.to_html(index=False)

st.markdown(table_html, unsafe_allow_html=True)

######################################################

# 7. Gráfico de lineas que permita seleccionar dos usuarios para comparar sus puntajes a lo largo del tiempo.

st.markdown("---")

text = "Comparativa de puntajes históricos de dos usuarios ⚖️ "
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

df_matches = pd.DataFrame(matches)

# Lista de usuarios que jugaron alguna vez
users = df_matches['usuario'].unique().tolist()

# Selección de usuarios
with st.form(key='user_selection_form'):
    selected_users = st.multiselect('👤 Seleccione dos usuarios:', users)
    submit_button = st.form_submit_button(label='Aceptar')

if submit_button:
    if len(selected_users) != 2:
        st.warning("Por favor, seleccione exactamente dos usuarios.")
    else:
        # Filtra el DataFrame para incluir solo los usuarios seleccionados
        filtered_df = df_matches[df_matches['usuario'].isin(selected_users)]

        # Convierte la columna de fecha y hora a datetime
        filtered_df['fecha_y_hora_inicio'] = pd.to_datetime(
            filtered_df['fecha_y_hora_inicio'])

        # Agrupa por usuario y fecha, calculando el puntaje promedio por día
        grouped_df = filtered_df.groupby(['usuario', filtered_df['fecha_y_hora_inicio'].dt.date]).agg({
            'puntaje': 'mean'}).reset_index()

        # Crea el gráfico de líneas
        fig, ax = plt.subplots()
        for user in selected_users:
            user_data = grouped_df[grouped_df['usuario'] == user]
            # Grafica el puntaje promedio por día y ajusta el gráfico
            ax.plot(user_data['fecha_y_hora_inicio'],
                    user_data['puntaje'], marker='o', label=user, alpha=0.7)
        ax.set_ylabel('Puntaje')
        ax.set_title('Evolución del puntaje por partida')
        ax.legend(title='Usuario')
        plt.xticks(rotation=45)
        st.pyplot(fig)

######################################################

# 8. Listar para cada género cuál es la temática en la cual demuestra mayor conocimiento.

st.markdown("---")
text = "Temática por género que demuestra mayor conocimiento en base a las respuestas correctas 🧠📚"
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

# Crea un diccionario para almacenar las respuestas correctas por temática y género
respuestas_por_genero_y_tematica = {}

generos = ['Masculino', 'Femenino', 'Otro', 'Prefiero no decirlo']

# Procesa el JSON de partidas
for partida in matches:
    tematica = partida["tematica"]
    respuestas_correctas = partida["respuestas_correctas"]
    # Extrae el email del usuario de la partida
    usuario_email = partida["usuario"].split(" ")[-1][1:-1]
    genero = usuarios_data[usuario_email]["gender"]

    # Si la temática no está en el diccionario, la inicializa
    if tematica not in respuestas_por_genero_y_tematica:
        respuestas_por_genero_y_tematica[tematica] = {
            genero: [] for genero in generos}

    # Agrega las respuestas correctas al género correspondiente
    respuestas_por_genero_y_tematica[tematica][genero].append(
        respuestas_correctas)

# Calcula el promedio de respuestas correctas para cada género por temática
tematica_con_mas_conocimiento_por_genero = {}
for tematica, generos in respuestas_por_genero_y_tematica.items():
    for genero, respuestas in generos.items():
        if len(respuestas) > 0:
            promedio = sum(respuestas) / len(respuestas)
            if genero not in tematica_con_mas_conocimiento_por_genero:
                tematica_con_mas_conocimiento_por_genero[genero] = {
                    "tematica": tematica, "promedio": promedio}
            else:
                if promedio > tematica_con_mas_conocimiento_por_genero[genero]["promedio"]:
                    tematica_con_mas_conocimiento_por_genero[genero] = {
                        "tematica": tematica, "promedio": promedio}

# Convierte el diccionario en un DataFrame
df = pd.DataFrame.from_dict(
    tematica_con_mas_conocimiento_por_genero, orient='index')

# Añade la columna 'Género'
df['Género'] = df.index

# Renombra las columnas y las ordena
df = df.rename(columns={'tematica': 'Temática', 'promedio': 'Promedio'})
df = df[['Género', 'Temática', 'Promedio']]

# Grafica
table_html = df.to_html(index=False)
st.markdown(table_html, unsafe_allow_html=True)

######################################################

# 9. Listar cada dificultad del juego con el puntaje promedio obtenido y con la cantidad de veces que fue elegida

st.markdown("---")
text = "Dificultades de juego con puntaje promedio y cantidad de veces elegida 🎮"
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

diccionario_dificultades = {
    "🟢": "Fácil 🟢",
    "🟡": "Media 🟡",
    "🔴": "Alta 🔴"
}


def map_dificultad(texto):
    for emoji, dificultad in diccionario_dificultades.items():
        if emoji in texto:
            return f"{dificultad}"


# Crea un diccionario para almacenar los puntajes por dificultad
puntajes_por_dificultad = defaultdict(list)
conteo_dificultad = defaultdict(int)

# Procesa el JSON de partidas para extraer la dificultad y puntaje
for partida in matches:
    dificultad = partida["dificultad"]
    puntaje = partida["puntaje"]

    # Agrega el puntaje a la lista correspondiente de la dificultad
    puntajes_por_dificultad[dificultad].append(puntaje)
    # Incrementa el conteo para la dificultad
    conteo_dificultad[dificultad] += 1

# Calcula el puntaje promedio por dificultad
promedio_puntaje_por_dificultad = {}
for dificultad, puntajes in puntajes_por_dificultad.items():
    promedio = sum(puntajes) / len(puntajes)
    promedio_puntaje_por_dificultad[dificultad] = promedio

# Crea un DataFrame con la dificultad, puntaje promedio y conteo
data_dificultad = {
    "Dificultad": list(promedio_puntaje_por_dificultad.keys()),
    "Puntaje Promedio": list(promedio_puntaje_por_dificultad.values()),
    "Cantidad de Veces Elegida": [conteo_dificultad[dificultad] for dificultad in promedio_puntaje_por_dificultad.keys()]
}

df_dificultad = pd.DataFrame(data_dificultad)
df_dificultad['Dificultad'] = df_dificultad['Dificultad'].apply(map_dificultad)

# Grafica
table_html = df_dificultad.to_html(index=False)
st.markdown(table_html, unsafe_allow_html=True)

######################################################

# 10. Listar los usuarios que registran una partida con un puntaje mayor a 0 en todos los días durante los ultimos 7 dias

st.markdown("---")
text = "Listado de usuarios en racha 🏆🔥"
subtitle = bold_text(text)
st.markdown(subtitle, unsafe_allow_html=True)

df = pd.DataFrame(matches)
df['fecha_y_hora_inicio'] = pd.to_datetime(df['fecha_y_hora_inicio'])

#  Obtiene la fecha actual y la normaliza para dejar solo la fecha
current_date = pd.to_datetime('today').normalize()

# Obtiene la fecha hace 7 días
last_week_date = current_date - pd.Timedelta(days=7)

# Selecciona las partidas que ocurrieron en los últimos 7 días
matches_last_week = df.loc[df['fecha_y_hora_inicio'] >= last_week_date]
users_positive_score = matches_last_week[matches_last_week['puntaje'] > 0]

# Agrupa por usuario y verifica que haya jugado los 7 días
mask = users_positive_score.groupby(
    'usuario')['fecha_y_hora_inicio'].nunique() == 7

# Lista de usuarios que cumplen con la condición
users_on_streak = mask[mask].index.tolist()
if len(users_on_streak) != 0:
    table_data = pd.DataFrame(users_on_streak, columns=["Usuarios en racha"])
    # Convertir DataFrame a HTML sin índices
    table_html = table_data.to_html(index=False, justify='center')

    # Renderizar la tabla centrada horizontalmente
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.write(
        "No hay usuarios en racha en los últimos 7 días. ¡Pero puedes ser el primero 🤩! ")
