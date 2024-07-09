def sanitize_text(text):
    """Convierte el texto a minúsculas y elimina los acentos diacríticos."""
    text = text.lower()
    accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
    sanitized_text = "".join(accents.get(char, char) for char in text)
    return sanitized_text


def classify_elevation(row):
    """Clasifica la elevación de un aeropuerto en una de tres categorías: bajo, medio o alto."""
    if row['elevation_ft'] != "":
        elevation = int(row['elevation_ft'])
    else:
        elevation = 0

    if elevation <= 131:
        elevation_name = 'bajo'
    elif elevation <= 903:
        elevation_name = 'medio'
    else:
        elevation_name = 'alto'
    return elevation_name


def classify_size(surface_km2):
    """Función para categorizar el tamaño del lago según su superficie en km²."""
    if surface_km2 <= 17:
        return "chico"
    elif 17 < surface_km2 <= 59:
        return "medio"
    else:
        return "grande"


def convert_gms_to_gd(gms_coordinate):
    """Función para convertir una coordenada de GMS a GD."""
    parts = gms_coordinate.split("°")
    degrees = float(parts[0])
    minutes = float(parts[1].split("'")[0])
    seconds = float(parts[1].split("'")[1].split("\"")[0])
    # Obtener la dirección (N/S para latitud, E/O para longitud)
    direction = parts[1].split("'")[1].split("\"")[1]

    # Calcular la coordenada en grados decimales (GD)
    gd_coordinate = degrees + (minutes / 60) + (seconds / 3600)

    # Aplicar la dirección (N/S para latitud, E/O para longitud)
    if direction in ['S', 'O']:
        gd_coordinate = -gd_coordinate  # Coordenadas en el hemisferio sur u oeste

    return gd_coordinate


def replace_invalid_values(value):
    """Reemplazar los valores "///" y "-" por cero."""
    if value == "///" or value == "-":
        return "0"
    else:
        return value


def calculate_porcentaje_situacion_calle(row):
    """Calcular el porcentaje de población en situación de calle."""
    total_population = int(row['Total de población'])
    homeless_population = int(row['Población en situación de calle(²)'])
    percentage = (homeless_population / total_population) * 100
    return percentage
