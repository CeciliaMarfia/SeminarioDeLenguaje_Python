from pathlib import Path
import sys
import streamlit as st
import json
from datetime import datetime
st.set_page_config(page_title='Formulario de Registro 📁')

cwd = Path('.').resolve()
sys.path.append(str(cwd))

# Cargar los datasets
from paths import USER_DB_PATH  # noqa


def form_page():
    with st.form(key="registration_form"):
        st.title('Formulario de Registro 📁')
        st.write('Completa el formulario para registrarte:')
        user_name = st.text_input('Nombre de Usuario')
        full_name = st.text_input('Nombre Completo')
        mail = st.text_input('Correo Electrónico')
        date_of_birth = st.date_input('Fecha de Nacimiento',
                                      min_value=datetime(1900, 1, 1),
                                      max_value=datetime.now())
        gender = st.radio(
            'Género', ['Masculino', 'Femenino', 'Otro', 'Prefiero no decirlo'])

        submitted = st.form_submit_button("Registrarse")

        if submitted:
            fields = [user_name, full_name,
                      mail, date_of_birth, gender]

            if any(field == '' for field in fields):
                st.warning('⚠️ Todos los campos deben ser completados.')
                return

            # Intentamos cargar los datos del archivo JSON
            try:
                with open(USER_DB_PATH, 'r') as infile:
                    json_object_load = json.load(infile)
                if mail in json_object_load.keys():
                    json_object_load[mail] = {
                        'username': user_name,
                        'name_surname': full_name,
                        'dob': str(date_of_birth),
                        'gender': gender
                    }
                    with open(USER_DB_PATH, "w") as outfile:
                        json.dump(json_object_load, outfile, indent=4)
                    st.success('✅ ¡Información actualizada exitosamente!')
                    return
            except FileNotFoundError:
                # Si el archivo no existe, inicializamos un diccionario vacío
                json_object_load = {}

            user = {'username': user_name,
                    'name_surname': full_name,
                    'dob': str(date_of_birth),
                    'gender': gender,
                    }

            # Si no existe el usuario lo agrego
            json_object_load[mail] = user

            with open(USER_DB_PATH, "w") as outfile:
                json.dump(json_object_load, outfile, indent=4)

            st.success('✅ ¡Registro exitoso!')


form_page()
