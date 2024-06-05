import unicodedata
import re
from src.database.connection import get_connection


# Función para normalizar texto
def normalize_text(text):
    # Convertir a minúsculas y normalizar a forma compuesta NFC
    text = text.lower()
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')


# Función para extraer n-gramas de múltiples columnas específicas
def extract_ngrams_from_columns(conn, table, columns, n):
    cur = conn.cursor()
    query = f"SELECT {', '.join(columns)} FROM {table}"
    cur.execute(query)
    while True:
        rows = cur.fetchmany(1000)
        if not rows:
            break
        for row in rows:
            for value in row:
                normalized_value = normalize_text(value)
                ngrams = extract_ngrams(normalized_value, n)
                for ngram in ngrams:
                    yield ngram
    cur.close()


def extract_ngrams(text, n):
    # Dividir el texto en palabras basándose en espacios, saltos de línea, tabulaciones, etc.
    words = re.split(r'\s+', text)
    return zip(*[words[i:] for i in range(n)])


# Función para limpiar palabras eliminando signos de puntuación finales
def clean_ngram(ngram):
    return tuple(re.sub(r'[.,:;!?]+$', '', word) for word in ngram)


# Función para obtener n-gramas únicos de dos generadores de n-gramas
def get_unique_ngrams(ngrams1, ngrams2):
    clean_ngrams = set()
    for ngram in ngrams1:
        clean_ngrams.add(clean_ngram(ngram))
    for ngram in ngrams2:
        clean_ngrams.add(clean_ngram(ngram))
    return clean_ngrams


# Función para guardar n-gramas únicos en un archivo TXT
def save_ngrams_to_txt(ngrams, filename):
    with open(filename, 'w') as f:
        for ngram in sorted(ngrams):
            f.write(' '.join(ngram) + '\n')


# Conectar a ambas bases de datos y extraer n-gramas
print("Conectando a la base de datos 1...")
conn1 = get_connection("computrabajo")
print("Conectando a la base de datos 2...")
conn2 = get_connection("elempleo")

# Especificar las columnas a extraer
columns_db1 = ['title']
columns_db2 = ['titulo']

# Obtener n-gramas únicos para n de 1 a 3 y guardarlos en archivos
for n in range(1, 4):
    print(f"Extrayendo {n}-gramas de la base de datos 1...")
    ngrams_db1 = extract_ngrams_from_columns(conn1, 'job_listings', columns_db1, n)
    print(f"Extrayendo {n}-gramas de la base de datos 2...")
    ngrams_db2 = extract_ngrams_from_columns(conn2, 'job_listings', columns_db2, n)

    print(f"Obteniendo {n}-gramas únicos...")
    unique_ngrams = get_unique_ngrams(ngrams_db1, ngrams_db2)

    # Guardar n-gramas únicos en un archivo TXT
    filename = f'unique_{n}grams.txt'
    print(f"Guardando {n}-gramas únicos en {filename}...")
    save_ngrams_to_txt(unique_ngrams, filename)

# Cerrar conexiones
print("Cerrando conexión a la base de datos 1...")
conn1.close()
print("Cerrando conexión a la base de datos 2...")
conn2.close()

print("Proceso completado.")
