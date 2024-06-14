# import unicodedata
# import re
# from src.database.connection import get_connection
#
# def normalize_text(text):
#     # Convertir a minúsculas y normalizar a forma compuesta NFC
#     text = text.lower()
#     return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
#
#
# # Función para extraer n-gramas de múltiples columnas específicas
# def extract_ngrams_from_columns(conn, table, columns, n):
#     cur = conn.cursor()
#     query = f"SELECT {', '.join(columns)} FROM {table}"
#     cur.execute(query)
#     while True:
#         rows = cur.fetchmany(100)
#         if not rows:
#             break
#         for row in rows:
#             for value in row:
#                 normalized_value = normalize_text(value)
#                 ngrams = extract_ngrams(normalized_value, n)
#                 for ngram in ngrams:
#                     yield ngram
#     cur.close()
#
# def extract_ngrams(text, n):
#     # Dividir el texto en palabras eliminando espacios extras y filtrando elementos vacíos
#     words = [word for word in re.split(r'\s+', text.strip()) if word]
#     # Generar n-gramas asegurando que todas las posiciones en el rango tienen suficientes palabras
#     if len(words) >= n:
#         return zip(*[words[i:] for i in range(n)])
#     return []  # Devuelve una lista vacía si no hay suficientes palabras para formar un n-grama
#
#
#
# # Función para limpiar palabras eliminando signos de puntuación finales
# def clean_ngram(ngram):
#     return tuple(re.sub(r'[.,:;!?]+$', '', word) for word in ngram)
#
#
# # Función para obtener n-gramas únicos de dos generadores de n-gramas
# def get_unique_ngrams(ngrams1, ngrams2):
#     clean_ngrams = set()
#     for ngram in ngrams1:
#         clean_ngrams.add(clean_ngram(ngram))
#     for ngram in ngrams2:
#         clean_ngrams.add(clean_ngram(ngram))
#     return clean_ngrams
#
#
# # Función para guardar n-gramas únicos en un archivo TXT
# def save_ngrams_to_txt(ngrams, filename):
#     with open(filename, 'w') as f:
#         for ngram in sorted(ngrams):
#             f.write(' '.join(ngram) + '\n')
#
#
# # Conectar a ambas bases de datos y extraer n-gramas
# print("Conectando a la base de datos 1...")
# conn1 = get_connection("computrabajo")
# print("Conectando a la base de datos 2...")
# conn2 = get_connection("elempleo")
#
# # Especificar las columnas a extraer
# columns_db1 = ['title', 'content', 'industry', 'keywords']
# columns_db2 = ['titulo', 'descripcion']
#
# # Obtener n-gramas únicos para n de 1 a 3 y guardarlos en archivos
# for n in range(1, 4):
#     print(f"Extrayendo {n}-gramas de la base de datos 1...")
#     ngrams_db1 = extract_ngrams_from_columns(conn1, 'job_listings', columns_db1, n)
#     print(f"Extrayendo {n}-gramas de la base de datos 2...")
#     ngrams_db2 = extract_ngrams_from_columns(conn2, 'job_listings', columns_db2, n)
#
#     print(f"Obteniendo {n}-gramas únicos...")
#     unique_ngrams = get_unique_ngrams(ngrams_db1, ngrams_db2)
#
#     # Guardar n-gramas únicos en un archivo TXT
#     filename = f'unique_{n}grams.txt'
#     print(f"Guardando {n}-gramas únicos en {filename}...")
#     save_ngrams_to_txt(unique_ngrams, filename)
#
# # Cerrar conexiones
# print("Cerrando conexión a la base de datos 1...")
# conn1.close()
# print("Cerrando conexión a la base de datos 2...")
# conn2.close()
#
# print("Proceso completado.")
import unicodedata
import re
import csv
from src.database.connection import get_connection
from tqdm import tqdm

def protect_special_terms(text):
    # Proteger términos especiales con marcadores temporales
    text = text.replace('c++', 'cpp_specialtoken')
    text = text.replace('c#', 'csharp_specialtoken')
    return text

def normalize_text(text):
    # Aplica protección de términos especiales primero
    text = protect_special_terms(text)
    # Convertir a minúsculas y normalizar a forma compuesta NFC, luego codificar y decodificar para eliminar tildes
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Reemplazar todos los caracteres no alfanuméricos por un espacio, excepto los marcadores especiales
    text = re.sub(r'(?<!_SPECIALTOKEN)\W+', ' ', text)
    # Restaura los términos especiales a su forma original
    text = text.replace('cpp_specialtoken', 'C++')
    text = text.replace('csharp_specialtoken', 'C#')
    # Elimina espacios adicionales que puedan haberse creado
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_ngrams(text, n):
    words = text.split()
    if len(words) >= n:
        return list(zip(*[words[i:] for i in range(n)]))
    return []

def extract_ngrams_from_columns(conn, table, columns, n):
    cur = conn.cursor()
    query = f"SELECT {', '.join(columns)} FROM {table}"
    cur.execute(query)
    rows = cur.fetchall()  # Carga todo el conjunto de datos de una vez
    all_ngrams = []
    for row in tqdm(rows, desc=f"Procesando n-gramas para n={n}"):
        full_text = ' '.join(row)  # Concatena todas las columnas en una sola cadena
        normalized_value = normalize_text(full_text)
        ngrams = extract_ngrams(normalized_value, n)
        all_ngrams.extend(ngrams)
    cur.close()
    return all_ngrams

def count_ngrams(ngrams):
    ngram_counts = {}
    for ngram in ngrams:
        ngram = tuple(ngram)  # Convert to tuple for dictionary key compatibility
        if ngram in ngram_counts:
            ngram_counts[ngram] += 1
        else:
            ngram_counts[ngram] = 1
    return ngram_counts

def save_ngrams_to_csv(ngrams_counts, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['N-gram', 'Count'])
        for ngram, count in sorted(ngrams_counts.items()):
            writer.writerow([' '.join(ngram), count])

def main():
    conn1 = get_connection("computrabajo")
    conn2 = get_connection("elempleo")
    columns_db1 = ['title', 'content', 'industry', 'keywords']
    columns_db2 = ['titulo', 'descripcion']

    for n in range(1, 2):
        ngrams_db1 = extract_ngrams_from_columns(conn1, 'job_listings', columns_db1, n)
        ngrams_count1 = count_ngrams(ngrams_db1)

        ngrams_db2 = extract_ngrams_from_columns(conn2, 'job_listings', columns_db2, n)
        ngrams_count2 = count_ngrams(ngrams_db2)

        all_ngrams = {**ngrams_count1, **ngrams_count2}
        for ngram, count in ngrams_count2.items():
            if ngram in all_ngrams:
                all_ngrams[ngram] += count
            else:
                all_ngrams[ngram] = count

        filename = f"ngram_counts_{n}.csv"
        print(f"Guardando conteos de {n}-gramas en {filename}...")
        save_ngrams_to_csv(all_ngrams, filename)

    conn1.close()
    conn2.close()
    print("Proceso completado.")

if __name__ == "__main__":
    main()

