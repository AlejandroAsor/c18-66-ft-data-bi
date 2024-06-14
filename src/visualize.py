import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://alejandroasorcorralesgomez:@localhost/keywords')

def load_statistics(keyword):
    keyword = f"%{keyword}%"
    query = """
    SELECT * FROM general_statistics
    WHERE keyword LIKE %(keyword)s;
    """
    return pd.read_sql(query, engine, params={"keyword": keyword})

st.title('Búsqueda de Palabras Clave en Estadísticas Generales')

keyword_input = st.text_input('Ingrese la palabra clave para buscar:')

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

