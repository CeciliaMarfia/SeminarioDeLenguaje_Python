import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

def generate_airports_map(df_airports):
   # Genera y muestra un mapa de los aeropuertos en Argentina, categorizados por niveles de elevación.
    st.title("✈️ Mapa de aeropuertos en Argentina")
    st.write("A través de sus coordenadas el siguiente mapa muestra los aeropuertos diferenciando los puntos por color según su elevación, siendo:")
    st.write('🟦 Bajo', '🟩 Medio', '🟥 Alto')
    # Crear un nuevo DataFrame con las columnas "latitude" y "longitude"
    airports_locations = df_airports[[
        'latitude_deg', 'longitude_deg', 'elevation_name']].copy()
    airports_locations.rename(
        columns={'latitude_deg': 'lat', 'longitude_deg': 'lon'}, inplace=True)

    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    m = folium.Map(
        location=(-33.457606, -65.346857),
        control_scale=True,
        zoom_start=5,
        name='es',
        tiles=tiles,
        attr=attr
    )
    # Elimina el aeropuerto que tiene lat/lon 0.001300  -0.001300 (mal cargado)
    airports_locations = airports_locations.drop(180)
    color_dict = {'bajo': 'blue', 'medio': 'green', 'alto': 'red'}
    for index, row in airports_locations.iterrows():
        color = color_dict.get(row['elevation_name'], 'gray')
        folium.Marker(location=[row['lat'], row['lon']],
                      icon=folium.Icon(color=color)).add_to(m)
    st_map = st_folium(m, width=700, height=450)

def generate_airports_per_province_chart(df_airports):
    # Genera y muestra un gráfico de barras con la cantidad de aeropuertos por provincia en Argentina.
    count_by_province = df_airports['region_name'].value_counts()

    st.title("🇦🇷 Cantidad de aeropuertos por provincia")
    st.bar_chart(count_by_province, color='#008080')

def generate_highest_elevation_airports_table(df_airports):
   # Genera y muestra una tabla con los aeropuertos de mayor elevación en Argentina.
    top_elevation = df_airports.nlargest(10, 'elevation_ft')

    st.title("📊 Tabla de aeropuertos con mayor elevación")

    # Personalizar el color de fondo y el color del texto de la tabla
    st.table(top_elevation.style
             .set_properties(**{'background-color': 'skyblue', 'color': 'black'})
             .set_table_styles([{'selector': 'tr:hover', 'props': [('background-color', 'lightblue')]}]))

def generate_lagos_map(df_lagos):
    # Genera y muestra un mapa de los lagos en Argentina con sus ubicaciones
    st.title("🌎 Mapa de lagos en Argentina")

    # Crear un nuevo DataFrame con las columnas "Latitud GD" y "Longitud GD"
    lagos_locations = df_lagos[['Latitud GD', 'Longitud GD', 'Nombre']].copy()
    lagos_locations.rename(
        columns={'Latitud GD': 'lat', 'Longitud GD': 'lon'}, inplace=True)

    # Mostrar el mapa
    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    m = folium.Map(
        location=(-38.416097, -63.616672),
        control_scale=True,
        zoom_start=5,
        name='es',
        tiles=tiles,
        attr=attr
    )
    for index, row in lagos_locations.iterrows():
        folium.Marker(location=[row['lat'], row['lon']],
                      popup=row['Nombre'],
                      icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
    st_map = st_folium(m, width=700, height=450)

def generate_depth_histogram(df_lagos):
    # Genera y muestra un histograma de la profundidad máxima de los lagos en Argentina.
    st.title("📊 Histograma de profundidad máxima de los lagos")

    plt.figure(figsize=(10, 6))
    df_lagos_profundidad = df_lagos['Profundidad máxima (m)'].dropna()
    plt.hist(df_lagos_profundidad,
             bins=20, color='#E6E6FA', edgecolor='blue')
    plt.xlabel('Profundidad máxima (m)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de la profundidad máxima de los lagos')
    st.pyplot(plt)


def generate_surface_by_size_chart(df_lagos):
    # Genera y muestra un gráfico de barras con la superficie de los lagos agrupados por tamaño en Argentina.
    st.title("🌊 Superficie de los Lagos por Tamaño")
    # Agrupar los datos por 'Sup Tamaño' y sumar la 'Superficie (km²)'
    surface_by_size = df_lagos.groupby('Sup Tamaño')['Superficie (km²)'].sum()

    st.bar_chart(surface_by_size, color='#E6E6FA')