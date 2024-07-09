import streamlit as st
from pathlib import Path
import sys
import pandas as pd

cwd = Path('.').resolve()
sys.path.append(str(cwd))

from paths import AR_AIRPORTS_COPY_DATA  # noqa
from paths import LAGOS_COPY_DATA  # noqa
from helpers.conociendo_nuestros_datos_helpers import *  # noqa

df_airports = pd.read_csv(AR_AIRPORTS_COPY_DATA)
df_lagos = pd.read_csv(LAGOS_COPY_DATA)


def page_data():
    st.title('Conociendo nuestros datos 🗂️')
    st.write('En esta sección, se presentarán gráficos, tablas y mapas que brinden información útil o interesante extraída de los conjuntos de datos utilizados como fuente para el juego.')


page_data()

# Invocaciones a funciones de los aeropuertos de argentina
generate_airports_map(df_airports)
generate_airports_per_province_chart(df_airports)
generate_highest_elevation_airports_table(df_airports)

# Invocaciones a funciones de los lagos de argentina
generate_lagos_map(df_lagos)
generate_depth_histogram(df_lagos)
generate_surface_by_size_chart(df_lagos)
