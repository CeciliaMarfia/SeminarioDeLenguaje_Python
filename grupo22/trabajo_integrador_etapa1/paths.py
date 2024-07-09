# Definimos la ruta de los archivos:
from pathlib import Path


# La ruta se resuelve usando resolve() para convertirla en una ruta absoluta, y luego
# se toma el directorio padre de esa ruta usando parent.
ROOT_DIR = Path(__file__).resolve().parent
DATASETS_DIR = ROOT_DIR / 'datasets'
AR_DATA = DATASETS_DIR / 'ar.csv'
AR_AIRPORTS_DATA = DATASETS_DIR / 'ar-airports.csv'
C2022_RESUMEN_DATA = DATASETS_DIR / 'c2022_tp_c_resumen_adaptado.csv'
CONECTIVIDAD_DATA = DATASETS_DIR/'Conectividad_Internet.csv'
LAGOS_DATA = DATASETS_DIR/'lagos_arg.csv'


DATASETS_COPY_DIR = ROOT_DIR / DATASETS_DIR / 'processed_datasets'
# Define las rutas de los archivos copiados
AR_COPY_DATA = DATASETS_COPY_DIR / 'ar_copy.csv'
AR_AIRPORTS_COPY_DATA = DATASETS_COPY_DIR / 'ar-airports_copy.csv'
C2022_RESUMEN_COPY_DATA = DATASETS_COPY_DIR / \
    'c2022_tp_c_resumen_adaptado_copy.csv'
CONECTIVIDAD_COPY_DATA = DATASETS_COPY_DIR / 'Conectividad_Internet_copy.csv'
LAGOS_COPY_DATA = DATASETS_COPY_DIR / 'lagos_arg_copy.csv'

# Define la ruta del archivo de la base de datos de usuarios para el formulario de streamlit
USER_DB_PATH = ROOT_DIR / 'usuarios.json'
MATCH_DB_PATH = ROOT_DIR / 'partidas.json'

# Ruta para las imagenes
MEMES = ROOT_DIR / 'memes'
KUN_AGUERO_MEME_PATH = MEMES / 'kun_aguero_vamo_a_jugar.jpg'
AGUS_OLIA_PROFILE_PATH = MEMES / 'agus_olia.jpg'
SOLCI_ARROYO_PROFILE_PATH = MEMES / 'solci_arroyo.jpg'
CHECHU_MARFIA_PROFILE_PATH = MEMES / 'chechu_marfia.jpg'
LOGO_PATH = MEMES / 'logo.png'
