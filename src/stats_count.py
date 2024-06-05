import psycopg2
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

    # Crear tabla de estadísticas generales
    cur.execute("""
    CREATE TABLE IF NOT EXISTS general_statistics (
        keyword TEXT PRIMARY KEY,
        job_count INTEGER NOT NULL,
        avg_experience DOUBLE PRECISION,
        avg_salary_usd DOUBLE PRECISION,
        max_salary_usd DOUBLE PRECISION,
        min_salary_usd DOUBLE PRECISION
    );
    """)

    # Crear tabla de combinaciones de palabras clave
    cur.execute("""
    CREATE TABLE IF NOT EXISTS keyword_combinations (
        primary_keyword TEXT NOT NULL REFERENCES general_statistics(keyword),
        combined_keyword TEXT NOT NULL,
        job_count INTEGER NOT NULL,
        avg_experience DOUBLE PRECISION,
        avg_salary_usd DOUBLE PRECISION,
        max_salary_usd DOUBLE PRECISION,
        min_salary_usd DOUBLE PRECISION,
        PRIMARY KEY (primary_keyword, combined_keyword)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def calculate_general_statistics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT k.keyword, 
           COUNT(jk.job_id) AS job_count, 
           AVG(el.level_cleaned) AS avg_experience,
           s.amount_cleaned,
           lc.country
    FROM keywords k
    LEFT JOIN job_keywords jk ON k.id = jk.keyword_id
    LEFT JOIN job_listings jl ON jk.job_id = jl.id
    LEFT JOIN experience_levels el ON jl.experience_level_id = el.id
    LEFT JOIN salaries s ON jl.salary_id = s.id
    LEFT JOIN locations lc ON jl.location_id = lc.id
    GROUP BY k.keyword, s.amount_cleaned, lc.country;
    """)

    results = cur.fetchall()

    cur.execute("TRUNCATE TABLE keyword_combinations, general_statistics CASCADE;")

    statistics = {}

    for row in results:
        keyword, job_count, avg_experience, amount_cleaned, country = row
        conversion_rate = get_currency_conversion(country)
        salary_usd = amount_cleaned * conversion_rate if amount_cleaned is not None else None

        if keyword not in statistics:
            statistics[keyword] = {
                "job_count": 0,
                "total_experience": 0,
                "total_salary": 0,
                "max_salary": 0,
                "min_salary": float('inf'),
                "count_experience": 0,
                "count_salary": 0
            }

        statistics[keyword]["job_count"] += job_count
        if avg_experience is not None:
            statistics[keyword]["total_experience"] += avg_experience * job_count
            statistics[keyword]["count_experience"] += job_count
        if salary_usd is not None:
            statistics[keyword]["total_salary"] += salary_usd * job_count
            statistics[keyword]["count_salary"] += job_count
            if salary_usd > statistics[keyword]["max_salary"]:
                statistics[keyword]["max_salary"] = salary_usd
            if salary_usd < statistics[keyword]["min_salary"]:
                statistics[keyword]["min_salary"] = salary_usd

    for keyword, data in statistics.items():
        job_count = data["job_count"]
        avg_experience = data["total_experience"] / data["count_experience"] if data["count_experience"] > 0 else None
        avg_salary_usd = data["total_salary"] / data["count_salary"] if data["count_salary"] > 0 else None
        max_salary_usd = data["max_salary"] if data["count_salary"] > 0 else None
        min_salary_usd = data["min_salary"] if data["count_salary"] > 0 else None

        cur.execute("""
        INSERT INTO general_statistics (keyword, job_count, avg_experience, avg_salary_usd, max_salary_usd, min_salary_usd)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (keyword, job_count, avg_experience, avg_salary_usd, max_salary_usd, min_salary_usd))

    conn.commit()
    cur.close()
    conn.close()

def calculate_keyword_combinations():
    conn = get_connection()
    cur = conn.cursor()

    # Obtener todas las palabras clave
    cur.execute("SELECT keyword FROM general_statistics")
    keywords = [row[0] for row in cur.fetchall()]

    for primary_keyword in keywords:
        for combined_keyword in keywords:
            if primary_keyword != combined_keyword:
                cur.execute(f"""
                SELECT '{primary_keyword}' AS primary_keyword,
                       '{combined_keyword}' AS combined_keyword,
                       COUNT(jk.job_id) AS job_count, 
                       AVG(el.level_cleaned) AS avg_experience,
                       s.amount_cleaned,
                       lc.country
                FROM job_keywords jk
                JOIN job_keywords jk2 ON jk.job_id = jk2.job_id
                LEFT JOIN job_listings jl ON jk.job_id = jl.id
                LEFT JOIN experience_levels el ON jl.experience_level_id = el.id
                LEFT JOIN salaries s ON jl.salary_id = s.id
                LEFT JOIN locations lc ON jl.location_id = lc.id
                WHERE jk.keyword_id = (SELECT id FROM keywords WHERE keyword = %s)
                  AND jk2.keyword_id = (SELECT id FROM keywords WHERE keyword = %s)
                GROUP BY s.amount_cleaned, lc.country;
                """, (primary_keyword, combined_keyword))

                combo_results = cur.fetchall()

                combo_statistics = {
                    "job_count": 0,
                    "total_experience": 0,
                    "total_salary": 0,
                    "max_salary": 0,
                    "min_salary": float('inf'),
                    "count_experience": 0,
                    "count_salary": 0
                }

                for row in combo_results:
                    primary_keyword, combined_keyword, job_count, avg_experience, amount_cleaned, country = row
                    conversion_rate = get_currency_conversion(country)
                    salary_usd = amount_cleaned * conversion_rate if amount_cleaned is not None else None

                    combo_statistics["job_count"] += job_count
                    if avg_experience is not None:
                        combo_statistics["total_experience"] += avg_experience * job_count
                        combo_statistics["count_experience"] += job_count
                    if salary_usd is not None:
                        combo_statistics["total_salary"] += salary_usd * job_count
                        combo_statistics["count_salary"] += job_count
                        if salary_usd > combo_statistics["max_salary"]:
                            combo_statistics["max_salary"] = salary_usd
                        if salary_usd < combo_statistics["min_salary"]:
                            combo_statistics["min_salary"] = salary_usd

                if combo_statistics["job_count"] > 0:
                    avg_experience = combo_statistics["total_experience"] / combo_statistics["count_experience"] if combo_statistics["count_experience"] > 0 else None
                    avg_salary_usd = combo_statistics["total_salary"] / combo_statistics["count_salary"] if combo_statistics["count_salary"] > 0 else None
                    max_salary_usd = combo_statistics["max_salary"] if combo_statistics["count_salary"] > 0 else None
                    min_salary_usd = combo_statistics["min_salary"] if combo_statistics["count_salary"] > 0 else None

                    cur.execute("""
                    INSERT INTO keyword_combinations (primary_keyword, combined_keyword, job_count, avg_experience, avg_salary_usd, max_salary_usd, min_salary_usd)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (primary_keyword, combined_keyword, combo_statistics["job_count"], avg_experience, avg_salary_usd, max_salary_usd, min_salary_usd))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_statistics_tables()
    calculate_general_statistics()
    calculate_keyword_combinations()
