from src.database.connection import get_connection

# Tabla de conversión de divisas a USD
currency_conversion = {
    "Chile": 0.0011,
    "Guatemala": 0.13,
    "Mexico": 0.056,
    "El Salvador": 0.11428571,
    "Peru": 0.27,
    "Colombia": 0.00026,
    "Argentina": 0.0011,
    "Ecuador": 1,
    "Honduras": 0.040,
    "Uruguay": 0.026,
    "Costa Rica": 0.0019,
    "Nicaragua": 0.027,
    "Paraguay": 0.00013,
    "Panama": 1,
    "Bolivia": 0.14,
    "Venezuela": 0.00000027410759,
    "Republica Dominicana": 0.017
}

def get_currency_conversion(country):
    return currency_conversion.get(country, 1)  # Retorna 1 si no se encuentra la tasa de conversión

def create_statistics_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Crear tabla de estadísticas generales incluyendo conteos específicos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS general_statistics (
        keyword TEXT PRIMARY KEY,
        offer_count_title INTEGER DEFAULT 0,
        offer_count_content INTEGER DEFAULT 0,
        title_frequency INTEGER DEFAULT 0,
        content_frequency INTEGER DEFAULT 0
    );
    """)

    # Crear tabla de combinaciones de palabras clave
    cur.execute("""
    CREATE TABLE IF NOT EXISTS keyword_combinations (
        primary_keyword TEXT NOT NULL REFERENCES general_statistics(keyword),
        combined_keyword TEXT NOT NULL,
        job_count INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (primary_keyword, combined_keyword)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def calculate_general_statistics():
    conn = get_connection()
    cur = conn.cursor()

    # Aseguramos que se seleccionan correctamente las palabras clave de la tabla 'keywords'
    cur.execute("""
    INSERT INTO general_statistics (keyword, offer_count_title, title_frequency)
    SELECT k.keyword, COUNT(DISTINCT jk.job_id), SUM(jk.title_count)
    FROM job_keywords jk
    JOIN keywords k ON jk.keyword_id = k.id
    WHERE jk.title_count > 0
    GROUP BY k.keyword
    ON CONFLICT (keyword) DO UPDATE SET offer_count_title = EXCLUDED.offer_count_title, title_frequency = EXCLUDED.title_frequency;
    """)

    cur.execute("""
    INSERT INTO general_statistics (keyword, offer_count_content, content_frequency)
    SELECT k.keyword, COUNT(DISTINCT jk.job_id), SUM(jk.content_count)
    FROM job_keywords jk
    JOIN keywords k ON jk.keyword_id = k.id
    WHERE jk.content_count > 0
    GROUP BY k.keyword
    ON CONFLICT (keyword) DO UPDATE SET offer_count_content = EXCLUDED.offer_count_content, content_frequency = EXCLUDED.content_frequency;
    """)

    conn.commit()
    cur.close()
    conn.close()

def calculate_keyword_combinations():
    conn = get_connection()
    cur = conn.cursor()

    # Ahora incluyendo 'keywords' para obtener el texto real de la palabra clave
    cur.execute("""
    SELECT DISTINCT jk1.job_id, k1.keyword AS primary_keyword, k2.keyword AS combined_keyword
    FROM job_keywords jk1
    JOIN job_keywords jk2 ON jk1.job_id = jk2.job_id AND jk1.keyword_id != jk2.keyword_id
    JOIN keywords k1 ON jk1.keyword_id = k1.id
    JOIN keywords k2 ON jk2.keyword_id = k2.id
    WHERE jk1.title_count > 0
    """)
    results = cur.fetchall()

    # Contar combinaciones donde la palabra primaria está en el título
    for job_id, primary_keyword, combined_keyword in results:
        cur.execute("""
        INSERT INTO keyword_combinations (primary_keyword, combined_keyword, job_count)
        VALUES (%s, %s, 1)
        ON CONFLICT (primary_keyword, combined_keyword) DO UPDATE SET job_count = keyword_combinations.job_count + 1;
        """, (primary_keyword, combined_keyword))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_statistics_tables()
    calculate_general_statistics()
    calculate_keyword_combinations()
