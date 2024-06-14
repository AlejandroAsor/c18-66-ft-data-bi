from src.database.connection import get_connection

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

def create_currency_conversion_table():
    conn = get_connection()
    cur = conn.cursor()

    # Crear la tabla de conversión de divisas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS currency_conversion (
        country TEXT PRIMARY KEY,
        conversion_rate DOUBLE PRECISION NOT NULL
    );
    """)

    # Poblar la tabla con los datos de conversión de divisas
    for country, rate in currency_conversion.items():
        cur.execute("""
        INSERT INTO currency_conversion (country, conversion_rate)
        VALUES (%s, %s)
        ON CONFLICT (country) DO UPDATE SET conversion_rate = EXCLUDED.conversion_rate;
        """, (country, rate))

    conn.commit()
    cur.close()
    conn.close()

# Llamar a la función para crear y poblar la tabla
create_currency_conversion_table()

# Diccionario de palabras clave y sus variantes
keyword_variants = {
    "Python": ["python", "py"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "C#": ["c#", "csharp"],
    "C++": ["c++", "cpp"],
    "PHP": ["php"],
    "TypeScript": ["typescript", "ts"],
    "Swift": ["swift"],
    "Rust": ["rust"],
    "Objective-C": ["objective-c", "objc"],
    "Go": ["go", "golang"],
    "Kotlin": ["kotlin"],
    "Matlab": ["matlab"],
    "Dart": ["dart"],
    "Ruby": ["ruby"],
    "VBA": ["vba", "visual basic for applications"],
    "Powershell": ["powershell"],
    "Ada": ["ada"],
    "Scala": ["scala"],
    "Lua": ["lua"],
    "Abap": ["abap"],
    "Visual Basic": ["visual basic", "vb"],
    "Julia": ["julia"],
    "Perl": ["perl"],
    "Haskell": ["haskell"],
    "Groovy": ["groovy"],
    "Cobol": ["cobol"],
    "Delphi/Pascal": ["delphi", "pascal"],
    "Oracle": ["oracle"],
    "MySQL": ["mysql"],
    "SQL Server": ["sql server", "mssql", "microsoft sql server"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb"],
    "Microsoft Access": ["microsoft access", "access"],
    "Firebase": ["firebase"],
    "Redis": ["redis"],
    "Splunk": ["splunk"],
    "SQLite": ["sqlite"],
    "Elasticsearch": ["elasticsearch", "elastic search"],
    "MariaDB": ["mariadb"],
    "SAP HANA": ["sap hana", "hana"],
    "DynamoDB": ["dynamodb", "amazon dynamodb"],
    "DB2": ["db2", "ibm db2"],
    "Apache Hive": ["apache hive", "hive"],
    "Neo4j": ["neo4j"],
    "FileMaker": ["filemaker"],
    "Solr": ["solr", "apache solr"],
    "Firebird": ["firebird"],
    "Ingres": ["ingres"],
    "Sybase": ["sybase"],
    "Hbase": ["hbase"],
    "CouchBase": ["couchbase"],
    "Memcached": ["memcached"],
    "Riak": ["riak"],
    "Informix": ["informix", "ibm informix"],
    "CouchDB": ["couchdb"],
    "dBase": ["dbase"],
    "Netezza": ["netezza", "ibm netezza"],
    "Full-stack Developer": ["full-stack", "full stack", "fullstack"],
    "Back-end Developer": ["back-end", "backend", "back end"],
    "Front-end Developer": ["front-end", "frontend", "front end"],
    "Desktop or Enterprise Applications Developer": ["desktop developer", "enterprise applications developer", "desktop applications developer"],
    "Mobile Developer": ["mobile developer", "mobile app developer", "mobile applications developer"],
    "Engineering Manager": ["engineering manager", "manager engineering"],
    "Embedded Applications or Devices Developer": ["embedded developer", "embedded systems developer", "embedded applications developer"],
    "Data Scientist or Machine Learning Specialist": ["data scientist", "machine learning specialist", "ml specialist"],
    "DevOps Specialist": ["devops", "devops engineer", "devops specialist"],
    "Research & Development Role": ["r&d", "research and development"],
    "Senior Executive": ["c-suite", "vp", "senior executive"],
    "Data Engineer": ["data engineer", "ingeniero de datos"],
    "Cloud Infrastructure Engineer": ["cloud infrastructure engineer", "cloud engineer"],
    "Game or Graphics Developer": ["game developer", "graphics developer", "game and graphics developer"],
    "Data or Business Analyst": ["data analyst", "business analyst"],
    "System Administrator": ["system administrator", "sysadmin"],
    "Project Manager": ["project manager"],
    "QA or Test Developer": ["qa developer", "test developer", "quality assurance developer"],
    "Security Professional": ["security professional", "security engineer"],
    "Product Manager": ["product manager"],
    "Site Reliability Engineer": ["site reliability engineer", "sre"],
    "Developer Experience": ["developer experience", "devex"],
    "Blockchain Developer": ["blockchain developer", "blockchain engineer"],
    "Hardware Engineer": ["hardware engineer"],
    "Designer": ["designer", "graphic designer"],
    "Database Administrator": ["database administrator", "dba"],
    "Developer Advocate": ["developer advocate", "devrel"],
}

# Diccionario de categorías
keyword_categories = {
    "Python": "Programming Language",
    "Java": "Programming Language",
    "JavaScript": "Programming Language",
    "C#": "Programming Language",
    "C++": "Programming Language",
    "PHP": "Programming Language",
    "TypeScript": "Programming Language",
    "Swift": "Programming Language",
    "Rust": "Programming Language",
    "Objective-C": "Programming Language",
    "Go": "Programming Language",
    "Kotlin": "Programming Language",
    "Matlab": "Programming Language",
    "Dart": "Programming Language",
    "Ruby": "Programming Language",
    "VBA": "Programming Language",
    "Powershell": "Scripting Language",
    "Ada": "Programming Language",
    "Scala": "Programming Language",
    "Lua": "Programming Language",
    "Abap": "Programming Language",
    "Visual Basic": "Programming Language",
    "Julia": "Programming Language",
    "Perl": "Programming Language",
    "Haskell": "Programming Language",
    "Groovy": "Programming Language",
    "Cobol": "Programming Language",
    "Delphi/Pascal": "Programming Language",
    "Oracle": "Database",
    "MySQL": "Database",
    "SQL Server": "Database",
    "PostgreSQL": "Database",
    "MongoDB": "Database",
    "Microsoft Access": "Database",
    "Firebase": "Database",
    "Redis": "Database",
    "Splunk": "Database",
    "SQLite": "Database",
    "Elasticsearch": "Database",
    "MariaDB": "Database",
    "SAP HANA": "Database",
    "DynamoDB": "Database",
    "DB2": "Database",
    "Apache Hive": "Database",
    "Neo4j": "Database",
    "FileMaker": "Database",
    "Solr": "Database",
    "Firebird": "Database",
    "Ingres": "Database",
    "Sybase": "Database",
    "Hbase": "Database",
    "CouchBase": "Database",
    "Memcached": "Database",
    "Riak": "Database",
    "Informix": "Database",
    "CouchDB": "Database",
    "dBase": "Database",
    "Netezza": "Database",
    "Full-stack Developer": "Role",
    "Back-end Developer": "Role",
    "Front-end Developer": "Role",
    "Desktop or Enterprise Applications Developer": "Role",
    "Mobile Developer": "Role",
    "Engineering Manager": "Role",
    "Embedded Applications or Devices Developer": "Role",
    "Data Scientist or Machine Learning Specialist": "Role",
    "DevOps Specialist": "Role",
    "Research & Development Role": "Role",
    "Senior Executive": "Role",
    "Data Engineer": "Role",
    "Cloud Infrastructure Engineer": "Role",
    "Game or Graphics Developer": "Role",
    "Data or Business Analyst": "Role",
    "System Administrator": "Role",
    "Project Manager": "Role",
    "QA or Test Developer": "Role",
    "Security Professional": "Role",
    "Product Manager": "Role",
    "Site Reliability Engineer": "Role",
    "Developer Experience": "Role",
    "Blockchain Developer": "Role",
    "Hardware Engineer": "Role",
    "Designer": "Role",
    "Database Administrator": "Role",
    "Developer Advocate": "Role",
}

def create_statistics_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Crear o extender la tabla de estadísticas generales
    cur.execute("""
    CREATE TABLE IF NOT EXISTS general_statistics (
        keyword TEXT PRIMARY KEY,
        category TEXT,
        offer_count_title INTEGER DEFAULT 0,
        offer_count_content INTEGER DEFAULT 0,
        title_frequency INTEGER DEFAULT 0,
        content_frequency INTEGER DEFAULT 0,
        avg_salary_usd DOUBLE PRECISION DEFAULT 0,
        avg_experience DOUBLE PRECISION DEFAULT 0
    );
    """)

    # Asegurarse de que la columna 'category' exista en la tabla 'general_statistics'
    cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='general_statistics' AND column_name='category') THEN
            ALTER TABLE general_statistics ADD COLUMN category TEXT;
        END IF;
    END
    $$;
    """)

    # Crear tabla de estadísticas de variantes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS variant_statistics (
        variant TEXT PRIMARY KEY,
        primary_keyword TEXT NOT NULL REFERENCES general_statistics(keyword),
        category TEXT,
        offer_count_title INTEGER DEFAULT 0,
        offer_count_content INTEGER DEFAULT 0,
        title_frequency INTEGER DEFAULT 0,
        content_frequency INTEGER DEFAULT 0
    );
    """)

    # Asegurarse de que la columna 'category' exista en la tabla 'variant_statistics'
    cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='variant_statistics' AND column_name='category') THEN
            ALTER TABLE variant_statistics ADD COLUMN category TEXT;
        END IF;
    END
    $$;
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

def get_combined_keywords():
    combined_keywords = {}
    for primary_keyword, variants in keyword_variants.items():
        for variant in variants:
            combined_keywords[variant] = primary_keyword
    return combined_keywords

def calculate_general_statistics():
    conn = get_connection()
    try:
        cur = conn.cursor()

        combined_keywords = get_combined_keywords()

        for variant, primary_keyword in combined_keywords.items():
            category = keyword_categories.get(primary_keyword, "Unknown")
            # Inserta o actualiza los conteos de ofertas y frecuencias para los títulos en general_statistics
            cur.execute("""
            INSERT INTO general_statistics (keyword, category, offer_count_title, title_frequency)
            SELECT %s, %s, COUNT(DISTINCT jk.job_id), SUM(jk.title_count)
            FROM job_keywords jk
            JOIN keywords k ON jk.keyword_id = k.id
            WHERE jk.title_count > 0 AND k.keyword = %s
            GROUP BY k.keyword
            ON CONFLICT (keyword) DO UPDATE SET 
                offer_count_title = general_statistics.offer_count_title + EXCLUDED.offer_count_title, 
                title_frequency = general_statistics.title_frequency + EXCLUDED.title_frequency;
            """, (primary_keyword, category, variant))

            # Inserta o actualiza los conteos de ofertas y frecuencias para el contenido en general_statistics
            cur.execute("""
            INSERT INTO general_statistics (keyword, category, offer_count_content, content_frequency)
            SELECT %s, %s, COUNT(DISTINCT jk.job_id), SUM(jk.content_count)
            FROM job_keywords jk
            JOIN keywords k ON jk.keyword_id = k.id
            WHERE jk.content_count > 0 AND k.keyword = %s
            GROUP BY k.keyword
            ON CONFLICT (keyword) DO UPDATE SET 
                offer_count_content = general_statistics.offer_count_content + EXCLUDED.offer_count_content, 
                content_frequency = general_statistics.content_frequency + EXCLUDED.content_frequency;
            """, (primary_keyword, category, variant))

            # Inserta o actualiza los conteos de ofertas y frecuencias para los títulos en variant_statistics
            cur.execute("""
            INSERT INTO variant_statistics (variant, primary_keyword, category, offer_count_title, title_frequency)
            SELECT %s, %s, %s, COUNT(DISTINCT jk.job_id), SUM(jk.title_count)
            FROM job_keywords jk
            JOIN keywords k ON jk.keyword_id = k.id
            WHERE jk.title_count > 0 AND k.keyword = %s
            GROUP BY k.keyword
            ON CONFLICT (variant) DO UPDATE SET 
                offer_count_title = variant_statistics.offer_count_title + EXCLUDED.offer_count_title, 
                title_frequency = variant_statistics.title_frequency + EXCLUDED.title_frequency;
            """, (variant, primary_keyword, category, variant))

            # Inserta o actualiza los conteos de ofertas y frecuencias para el contenido en variant_statistics
            cur.execute("""
            INSERT INTO variant_statistics (variant, primary_keyword, category, offer_count_content, content_frequency)
            SELECT %s, %s, %s, COUNT(DISTINCT jk.job_id), SUM(jk.content_count)
            FROM job_keywords jk
            JOIN keywords k ON jk.keyword_id = k.id
            WHERE jk.content_count > 0 AND k.keyword = %s
            GROUP BY k.keyword
            ON CONFLICT (variant) DO UPDATE SET 
                offer_count_content = variant_statistics.offer_count_content + EXCLUDED.offer_count_content, 
                content_frequency = variant_statistics.content_frequency + EXCLUDED.content_frequency;
            """, (variant, primary_keyword, category, variant))

        # Calcular el salario promedio por variante
        variant_salaries = {}
        for primary_keyword, variants in keyword_variants.items():
            for variant in variants:
                cur.execute(f"""
                SELECT AVG(s.amount_cleaned * cc.conversion_rate) AS avg_salary_usd, COUNT(s.amount_cleaned)
                FROM job_listings jl
                JOIN salaries s ON jl.salary_id = s.id
                JOIN locations l ON jl.location_id = l.id
                JOIN currency_conversion cc ON l.country = cc.country
                JOIN job_keywords jk ON jl.id = jk.job_id
                JOIN keywords k ON jk.keyword_id = k.id
                WHERE s.amount_cleaned IS NOT NULL
                  AND (jk.title_count > 0 OR jk.content_count > 0)
                  AND k.keyword = '{variant}'
                GROUP BY k.keyword
                """)

                result = cur.fetchone()
                if result:
                    avg_salary_usd, count = result
                    if primary_keyword not in variant_salaries:
                        variant_salaries[primary_keyword] = {'total_salary_usd': 0, 'total_count': 0}
                    variant_salaries[primary_keyword]['total_salary_usd'] += avg_salary_usd * count
                    variant_salaries[primary_keyword]['total_count'] += count

        for primary_keyword, data in variant_salaries.items():
            avg_salary_usd = data['total_salary_usd'] / data['total_count'] if data['total_count'] > 0 else 0
            cur.execute("""
            UPDATE general_statistics
            SET avg_salary_usd = %s
            WHERE keyword = %s;
            """, (avg_salary_usd, primary_keyword))
            print(f"Updating salary for {primary_keyword} with average {avg_salary_usd}")  # Debug: print the update details

        # Calcular la experiencia promedio y actualizar la tabla general_statistics
        salary_conditions = []
        for primary_keyword, variants in keyword_variants.items():
            keyword_conditions = " OR ".join([f"k.keyword = '{variant}'" for variant in variants])
            salary_conditions.append(f"({keyword_conditions})")

        experience_query = f"""
        SELECT k.keyword, AVG(el.level_cleaned) AS avg_experience
        FROM job_listings jl
        JOIN experience_levels el ON jl.experience_level_id = el.id
        JOIN job_keywords jk ON jl.id = jk.job_id
        JOIN keywords k ON jk.keyword_id = k.id
        WHERE el.level_cleaned IS NOT NULL
          AND (jk.title_count > 0 OR jk.content_count > 0)
          AND {' OR '.join(salary_conditions)}
        GROUP BY k.keyword
        """

        print("Executing experience query:")
        print(experience_query)  # Debug: print the experience query to ensure correctness

        cur.execute(experience_query)
        rows = cur.fetchall()
        for keyword, avg_experience in rows:
            primary_keyword = combined_keywords.get(keyword, keyword)
            print(f"Updating experience for {primary_keyword} with average {avg_experience}")  # Debug: print the update details
            cur.execute("""
            UPDATE general_statistics
            SET avg_experience = %s
            WHERE keyword = %s;
            """, (avg_experience, primary_keyword))

        conn.commit()
        print("General statistics updated successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def calculate_keyword_combinations():
    conn = get_connection()
    cur = conn.cursor()

    combined_keywords = get_combined_keywords()

    # Obtener combinaciones de palabras clave teniendo en cuenta las variantes
    cur.execute("""
    SELECT DISTINCT jk1.job_id, k1.keyword AS primary_keyword, k2.keyword AS combined_keyword
    FROM job_keywords jk1
    JOIN job_keywords jk2 ON jk1.job_id = jk2.job_id AND jk1.keyword_id != jk2.keyword_id
    JOIN keywords k1 ON jk1.keyword_id = k1.id
    JOIN keywords k2 ON jk2.keyword_id = k2.id
    WHERE jk1.title_count > 0
    """)
    results = cur.fetchall()

    # Utilizar un diccionario para almacenar combinaciones únicas
    job_combinations = {}

    for job_id, primary_keyword, combined_keyword in results:
        primary_keyword = combined_keywords.get(primary_keyword, primary_keyword)
        combined_keyword = combined_keywords.get(combined_keyword, combined_keyword)

        if primary_keyword != combined_keyword:
            if (primary_keyword, combined_keyword) not in job_combinations:
                job_combinations[(primary_keyword, combined_keyword)] = set()
            job_combinations[(primary_keyword, combined_keyword)].add(job_id)

    for (primary_keyword, combined_keyword), job_ids in job_combinations.items():
        cur.execute("""
        INSERT INTO keyword_combinations (primary_keyword, combined_keyword, job_count)
        VALUES (%s, %s, %s)
        ON CONFLICT (primary_keyword, combined_keyword) DO UPDATE SET job_count = keyword_combinations.job_count + EXCLUDED.job_count;
        """, (primary_keyword, combined_keyword, len(job_ids)))

    conn.commit()
    cur.close()
    conn.close()
def calculate_country_statistics():
    conn = get_connection()
    cur = conn.cursor()

    combined_keywords = get_combined_keywords()

    for variant, primary_keyword in combined_keywords.items():
        category = keyword_categories.get(primary_keyword, "Unknown")
        # Consulta para calcular el conteo de ofertas y frecuencias por país con salarios y experiencia filtrados
        cur.execute("""
        SELECT l.country,
               COUNT(DISTINCT CASE WHEN jk.title_count > 0 THEN jk.job_id END) AS offer_count_title,
               COUNT(DISTINCT CASE WHEN jk.content_count > 0 THEN jk.job_id END) AS offer_count_content,
               SUM(jk.title_count) AS title_frequency,
               SUM(jk.content_count) AS content_frequency,
               AVG(CASE WHEN s.amount_cleaned * cc.conversion_rate BETWEEN 50 AND 10000 THEN s.amount_cleaned * cc.conversion_rate END) AS avg_salary_usd,
               AVG(CASE WHEN el.level_cleaned > 0 THEN el.level_cleaned END) AS avg_experience
        FROM job_keywords jk
        JOIN job_listings jl ON jl.id = jk.job_id
        JOIN keywords k ON jk.keyword_id = k.id
        JOIN locations l ON jl.location_id = l.id
        JOIN currency_conversion cc ON l.country = cc.country
        LEFT JOIN salaries s ON jl.salary_id = s.id
        LEFT JOIN experience_levels el ON jl.experience_level_id = el.id
        WHERE k.keyword = %s
        GROUP BY l.country
        """, (variant,))

        rows = cur.fetchall()
        for row in rows:
            country, offer_count_title, offer_count_content, title_frequency, content_frequency, avg_salary_usd, avg_experience = row
            # Asegurarse de actualizar los valores correctamente en la base de datos
            cur.execute("""
            INSERT INTO country_statistics (country, keyword, category, offer_count_title, offer_count_content, title_frequency, content_frequency, avg_salary_usd, avg_experience)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (country, keyword) DO UPDATE SET
                offer_count_title = country_statistics.offer_count_title + EXCLUDED.offer_count_title,
                offer_count_content = country_statistics.offer_count_content + EXCLUDED.offer_count_content,
                title_frequency = country_statistics.title_frequency + EXCLUDED.title_frequency,
                content_frequency = country_statistics.content_frequency + EXCLUDED.content_frequency,
                avg_salary_usd = COALESCE(EXCLUDED.avg_salary_usd, country_statistics.avg_salary_usd),
                avg_experience = COALESCE(EXCLUDED.avg_experience, country_statistics.avg_experience);
            """, (country, primary_keyword, category, offer_count_title, offer_count_content, title_frequency, content_frequency, avg_salary_usd, avg_experience))

    conn.commit()
    cur.close()
    conn.close()





if __name__ == "__main__":
    create_currency_conversion_table()
    create_statistics_tables()
    calculate_general_statistics()
    calculate_keyword_combinations()
    calculate_country_statistics()
