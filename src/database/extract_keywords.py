import re
from src.database.connection import get_connection

DB_CONFIG = {
    "computrabajo": ["title", "content", "keywords"],
    "elempleo": ["titulo", "descripcion"],
}

def fetch_jobs_with_keyword(keyword, db_type):
    """ Busca IDs de trabajos que contienen una palabra clave específica, usando regex de forma segura. """
    safe_keyword = re.escape(keyword)
    conn = get_connection(db_type=db_type)
    cur = conn.cursor()

    fields = DB_CONFIG.get(db_type, [])
    if not fields:
        raise ValueError(f"No hay configuración de campos para la base de datos: {db_type}")

    conditions = " OR ".join([f"{field} ~* '(?<![a-zA-Z]){safe_keyword}(?![a-zA-Z])'" for field in fields])
    query = f"SELECT id FROM job_listings WHERE {conditions}"

    cur.execute(query)
    job_ids = cur.fetchall()
    cur.close()
    conn.close()

    return [job_id[0] for job_id in job_ids]


def store_jobs_with_keyword(keyword, job_ids, source_db_id):
    """Almacena los IDs de trabajos relacionados con una palabra clave en la base de datos."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM keywords WHERE keyword = %s;", (keyword,))
    result = cur.fetchone()
    if not result:
        cur.execute("INSERT INTO keywords (keyword) VALUES (%s) RETURNING id;", (keyword,))
        keyword_id = cur.fetchone()[0]
    else:
        keyword_id = result[0]
    for job_id in job_ids:
        cur.execute("INSERT INTO job_keywords (job_id, keyword_id, source_db_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (job_id, keyword_id, source_db_id))
    conn.commit()
    cur.close()
    conn.close()

def get_source_db_id(db_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM source_database WHERE name = %s;", (db_name,))
    result = cur.fetchone()
    if not result:
        cur.execute("INSERT INTO source_database (name) VALUES (%s) RETURNING id;", (db_name,))
        source_db_id = cur.fetchone()[0]
    else:
        source_db_id = result[0]
    conn.commit()
    cur.close()
    conn.close()
    return source_db_id

def process_keywords_from_file(file_path, db_name):
    source_db_id = get_source_db_id(db_name)
    with open(file_path, 'r') as file:
        for line in file:
            keyword = line.strip().lower()
            if len(keyword) <= 1:
                continue
            job_ids = fetch_jobs_with_keyword(keyword, db_name)
            if job_ids:
                store_jobs_with_keyword(keyword, job_ids, source_db_id)
                print(f"Procesados {len(job_ids)} trabajos con la palabra clave '{keyword}' de la base de datos '{db_name}'.")
            else:
                print(f"No se encontraron trabajos que contengan la palabra clave '{keyword}' en la base de datos '{db_name}'.")

if __name__ == "__main__":
    process_keywords_from_file('keywords.txt', 'computrabajo')
