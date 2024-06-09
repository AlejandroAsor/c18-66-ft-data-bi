# import re
# from urllib.parse import urlparse
# from src.database.connection import get_connection
# from src.database.create import insert_if_not_exists, insert_location, link_keyword_to_job
#
# DB_CONFIG = {
#     "computrabajo": {
#         "fields": ["title", "content", "keywords"],
#         "experience_field": "experience_years_llama3_70b",
#         "salary_field": "salary",
#         "date_scraped_field": "date_scraped",
#         "date_posted_field": "date_posted"
#     },
#     "elempleo": {
#         "fields": ["titulo", "descripcion"],
#         "experience_field": "experiencia",
#         "salary_field": "salario",
#         "date_scraped_field": "date_scraped",
#         "date_posted_field": "fecha_publicacion"
#     },
# }
#
# def extract_country_from_url(url):
#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc
#     tld = domain.split('.')[0]
#     country_codes = {
#         "ar": "Argentina",
#         "bo": "Bolivia",
#         "cl": "Chile",
#         "co": "Colombia",
#         "cr": "Costa Rica",
#         "do": "Republica Dominicana",
#         "ec": "Ecuador",
#         "gt": "Guatemala",
#         "hn": "Honduras",
#         "mx": "Mexico",
#         "ni": "Nicaragua",
#         "pa": "Panama",
#         "pe": "Peru",
#         "pr": "Puerto Rico",
#         "py": "Paraguay",
#         "sv": "El Salvador",
#         "uy": "Uruguay",
#         "ve": "Venezuela",
#     }
#     return country_codes.get(tld, "Desconocido")
#
# def fetch_jobs_with_keyword(keyword, db_type):
#     """Busca IDs de trabajos que contienen una palabra clave específica, usando regex de forma segura."""
#     safe_keyword = re.escape(keyword)
#     conn = get_connection(db_type=db_type)
#     cur = conn.cursor()
#
#     config = DB_CONFIG.get(db_type)
#     if not config:
#         raise ValueError(f"No hay configuración de campos para la base de datos: {db_type}")
#
#     fields = config["fields"]
#     experience_field = config["experience_field"]
#     salary_field = config["salary_field"]
#     date_scraped_field = config["date_scraped_field"]
#     date_posted_field = config["date_posted_field"]
#
#     conditions = " OR ".join([f"{field} ~* '(?<![a-zA-Z]){safe_keyword}(?![a-zA-Z])'" for field in fields])
#     query = f"""
#         SELECT id, {experience_field} as experience_level, url, {salary_field}, {date_scraped_field}, {date_posted_field}
#         FROM job_listings
#         WHERE {conditions}
#     """
#
#     cur.execute(query)
#     jobs = cur.fetchall()
#     cur.close()
#     conn.close()
#
#     return jobs
#
#
# def insert_salary(amount):
#     conn = get_connection()
#     cur = conn.cursor()
#     try:
#         # Primero, verifica si el salario ya está en la tabla
#         cur.execute("SELECT id FROM salaries WHERE amount = %s;", (amount,))
#         salary_id = cur.fetchone()
#         if salary_id:
#             return salary_id[0]
#
#         # Si no está, inserta el salario
#         cur.execute("INSERT INTO salaries (amount) VALUES (%s) RETURNING id;", (amount,))
#         salary_id = cur.fetchone()[0]
#         return salary_id
#     except Exception as e:
#         print(f"Error inserting salary '{amount}': {e}")
#     finally:
#         conn.commit()
#         cur.close()
#         conn.close()
#
#
# def store_jobs_with_keyword(keyword, jobs, source_db_id):
#     """Almacena los IDs de trabajos relacionados con una palabra clave en la base de datos."""
#     conn = get_connection()
#     cur = conn.cursor()
#     keyword_id = insert_if_not_exists("keywords", "keyword", keyword)
#
#     for job in jobs:
#         job_id, experience_level, url, salary, date_scraped, date_posted = job
#         job_id = str(job_id)
#         if not experience_level:
#             experience_level = "Desconocido"
#
#         # Check if the job already exists
#         cur.execute("SELECT experience_level_id, location_id, salary_id FROM job_listings WHERE id = %s;", (job_id,))
#         existing_job = cur.fetchone()
#
#         if existing_job:
#             experience_level_id, location_id, salary_id = existing_job
#         else:
#             experience_level_id = insert_if_not_exists("experience_levels", "level", experience_level)
#             if source_db_id == get_source_db_id("elempleo"):
#                 country = "Colombia"
#             else:
#                 country = extract_country_from_url(url)
#             location_id = insert_location(country)
#             salary_id = insert_salary(salary)
#
#             cur.execute("""
#                 INSERT INTO job_listings (id, experience_level_id, source_db_id, location_id, salary_id, date_scraped, date_posted)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 ON CONFLICT (id) DO NOTHING;
#                 """, (job_id, experience_level_id, source_db_id, location_id, salary_id, date_scraped, date_posted))
#
#         link_keyword_to_job(keyword_id, job_id)
#
#     conn.commit()
#     cur.close()
#     conn.close()
#
# def get_source_db_id(db_name):
#     return insert_if_not_exists("source_database", "name", db_name)
#
# def process_keywords_from_file(file_path, db_name):
#     source_db_id = get_source_db_id(db_name)
#     with open(file_path, 'r') as file:
#         for line in file:
#             keyword = line.strip().lower()
#             if len(keyword) <= 1:
#                 continue
#             jobs = fetch_jobs_with_keyword(keyword, db_name)
#             if jobs:
#                 store_jobs_with_keyword(keyword, jobs, source_db_id)
#                 print(f"Procesados {len(jobs)} trabajos con la palabra clave '{keyword}' de la base de datos '{db_name}'.")
#             else:
#                 print(f"No se encontraron trabajos que contengan la palabra clave '{keyword}' en la base de datos '{db_name}'.")
#
# if __name__ == "__main__":
#     # process_keywords_from_file('keywords.txt', 'computrabajo')
#     process_keywords_from_file('keywords.txt', 'elempleo')
import re
from urllib.parse import urlparse
from src.database.connection import get_connection
from src.database.create import insert_if_not_exists, insert_location, link_keyword_to_job

DB_CONFIG = {
    "computrabajo": {
        "title_field": "title",
        "content_fields": ["content", "keywords"],
        "experience_field": "experience_years_llama3_70b",
        "salary_field": "salary",
        "date_scraped_field": "date_scraped",
        "date_posted_field": "date_posted"
    },
    "elempleo": {
        "title_field": "titulo",
        "content_fields": ["descripcion"],
        "experience_field": "experiencia",
        "salary_field": "salario",
        "date_scraped_field": "date_scraped",
        "date_posted_field": "fecha_publicacion"
    },
}

def extract_country_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    tld = domain.split('.')[0]
    country_codes = {
        "ar": "Argentina",
        "bo": "Bolivia",
        "cl": "Chile",
        "co": "Colombia",
        "cr": "Costa Rica",
        "do": "Republica Dominicana",
        "ec": "Ecuador",
        "gt": "Guatemala",
        "hn": "Honduras",
        "mx": "Mexico",
        "ni": "Nicaragua",
        "pa": "Panama",
        "pe": "Peru",
        "pr": "Puerto Rico",
        "py": "Paraguay",
        "sv": "El Salvador",
        "uy": "Uruguay",
        "ve": "Venezuela",
    }
    return country_codes.get(tld, "Desconocido")

def count_keyword_occurrences(text, keyword):
    """Cuenta cuántas veces aparece una palabra clave en un texto, insensible a mayúsculas."""
    pattern = re.compile(r'(?<![a-zA-Z])' + re.escape(keyword) + r'(?![a-zA-Z])', re.IGNORECASE)
    return len(pattern.findall(text))

def fetch_jobs_with_keyword(keyword, db_type):
    """Busca IDs de trabajos que contienen una palabra clave específica, usando regex de forma segura."""
    safe_keyword = re.escape(keyword)
    conn = get_connection(db_type=db_type)
    cur = conn.cursor()

    config = DB_CONFIG.get(db_type)
    if not config:
        raise ValueError(f"No hay configuración de campos para la base de datos: {db_type}")

    title_field = config["title_field"]
    content_fields = config["content_fields"]
    experience_field = config["experience_field"]
    salary_field = config["salary_field"]
    date_scraped_field = config["date_scraped_field"]
    date_posted_field = config["date_posted_field"]

    fields = [title_field] + content_fields
    content_conditions = " OR ".join([f"{field} ~* '(?<![a-zA-Z]){safe_keyword}(?![a-zA-Z])'" for field in content_fields])
    query = (
        f"SELECT id, {experience_field} as experience_level, url, {salary_field}, {date_scraped_field}, {date_posted_field}, "
        + ", ".join(fields) +
        f" FROM job_listings WHERE {title_field} ~* '(?<![a-zA-Z]){safe_keyword}(?![a-zA-Z])' OR {content_conditions}"
    )

    cur.execute(query)
    jobs = cur.fetchall()
    cur.close()
    conn.close()

    return jobs, title_field, content_fields

def insert_salary(amount):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Primero, verifica si el salario ya está en la tabla
        cur.execute("SELECT id FROM salaries WHERE amount = %s;", (amount,))
        salary_id = cur.fetchone()
        if salary_id:
            return salary_id[0]

        # Si no está, inserta el salario
        cur.execute("INSERT INTO salaries (amount) VALUES (%s) RETURNING id;", (amount,))
        salary_id = cur.fetchone()[0]
        return salary_id
    except Exception as e:
        print(f"Error inserting salary '{amount}': {e}")
    finally:
        conn.commit()
        cur.close()
        conn.close()

def store_jobs_with_keyword(keyword, jobs, source_db_id, title_field, content_fields):
    """Almacena los IDs de trabajos relacionados con una palabra clave en la base de datos."""
    conn = get_connection()
    cur = conn.cursor()
    keyword_id = insert_if_not_exists("keywords", "keyword", keyword)

    for job in jobs:
        job_id, experience_level, url, salary, date_scraped, date_posted, *fields = job
        job_id = str(job_id)
        if not experience_level:
            experience_level = "Desconocido"

        # Conteo de ocurrencias
        title_text = fields[0]
        content_texts = fields[1:]

        title_count = count_keyword_occurrences(title_text, keyword)
        content_count = sum(count_keyword_occurrences(text, keyword) for text in content_texts)

        # Check if the job already exists
        cur.execute("SELECT experience_level_id, location_id, salary_id FROM job_listings WHERE id = %s;", (job_id,))
        existing_job = cur.fetchone()

        if existing_job:
            experience_level_id, location_id, salary_id = existing_job
        else:
            experience_level_id = insert_if_not_exists("experience_levels", "level", experience_level)
            if source_db_id == get_source_db_id("elempleo"):
                country = "Colombia"
            else:
                country = extract_country_from_url(url)
            location_id = insert_location(country)
            salary_id = insert_salary(salary)

            cur.execute("""
                INSERT INTO job_listings (id, experience_level_id, source_db_id, location_id, salary_id, date_scraped, date_posted) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                ON CONFLICT (id) DO NOTHING;
                """, (job_id, experience_level_id, source_db_id, location_id, salary_id, date_scraped, date_posted))

        # Insert into job_keywords with the counts
        cur.execute("""
            INSERT INTO job_keywords (job_id, keyword_id, title_count, content_count) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (job_id, keyword_id) DO UPDATE 
            SET title_count = EXCLUDED.title_count, content_count = EXCLUDED.content_count;
            """, (job_id, keyword_id, title_count, content_count))

        print(f"Palabra clave '{keyword}' encontrada {title_count} veces en el título y {content_count} veces en el resto de las columnas para la oferta {job_id}.")

    conn.commit()
    cur.close()
    conn.close()

def get_source_db_id(db_name):
    return insert_if_not_exists("source_database", "name", db_name)

def process_keywords_from_file(file_path, db_name):
    source_db_id = get_source_db_id(db_name)
    with open(file_path, 'r') as file:
        for line in file:
            keyword = line.strip().lower()
            if len(keyword) <= 1:
                continue
            jobs, title_field, content_fields = fetch_jobs_with_keyword(keyword, db_name)
            if jobs:
                store_jobs_with_keyword(keyword, jobs, source_db_id, title_field, content_fields)
                print(f"Procesados {len(jobs)} trabajos con la palabra clave '{keyword}' de la base de datos '{db_name}'.")
            else:
                print(f"No se encontraron trabajos que contengan la palabra clave '{keyword}' en la base de datos '{db_name}'.")

if __name__ == "__main__":
    process_keywords_from_file('keywords.txt', 'computrabajo')
    process_keywords_from_file('keywords.txt', 'elempleo')
