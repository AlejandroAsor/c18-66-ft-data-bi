import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configura la conexión a la base de datos PostgreSQL
engine = create_engine('postgresql://alejandroasorcorralesgomez:@localhost/keywords')

# Función para cargar las estadísticas filtradas por palabra clave
def load_statistics(keyword):
    keyword = f"%{keyword}%"  # Prepara el keyword para la búsqueda con LIKE
    query = """
    SELECT * FROM general_statistics
    WHERE keyword LIKE %(keyword)s;
    """
    return pd.read_sql(query, engine, params={"keyword": keyword})

# Diseño de la aplicación en Streamlit
st.title('Búsqueda de Palabras Clave en Estadísticas Generales')

# Campo de entrada para la búsqueda de keywords
keyword_input = st.text_input('Ingrese la palabra clave para buscar:')

# Botón de búsqueda y visualización de resultados
if st.button('Buscar'):
    if keyword_input:
        results = load_statistics(keyword_input)
        if not results.empty:
            st.write('Resultados de la búsqueda:')
            st.dataframe(results)
        else:
            st.write('No se encontraron resultados para la palabra clave proporcionada.')
    else:
        st.write('Por favor, ingrese una palabra clave para buscar.')

