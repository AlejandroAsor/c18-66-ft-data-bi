from src.database.connection import get_connection

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS keywords (
            id SERIAL PRIMARY KEY,
            keyword TEXT UNIQUE NOT NULL,
            date_created TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            date_update TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS source_database (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            date_created TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS experience_levels (
            id SERIAL PRIMARY KEY,
            level TEXT UNIQUE NOT NULL,
            level_cleaned INTEGER
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            country TEXT UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS salaries (
            id SERIAL PRIMARY KEY,
            amount TEXT UNIQUE NOT NULL,
            amount_cleaned FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS job_listings (
            id VARCHAR(255) PRIMARY KEY,
            experience_level_id INTEGER REFERENCES experience_levels(id),
            source_db_id INTEGER REFERENCES source_database(id),
            location_id INTEGER REFERENCES locations(id),
            salary_id INTEGER REFERENCES salaries(id),
            date_scraped TEXT,
            date_posted TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS job_keywords (
            keyword_id INTEGER REFERENCES keywords(id),
            job_id VARCHAR(255) REFERENCES job_listings(id),
            title_count INTEGER,
            content_count INTEGER,
            PRIMARY KEY (keyword_id, job_id)
        );
        """
    ]
    conn = get_connection()
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()

def insert_if_not_exists(table, column, value):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT id FROM {table} WHERE {column} = %s;", (value,))
        result_id = cur.fetchone()
        if result_id:
            return result_id[0]
        else:
            query = f"INSERT INTO {table} ({column}) VALUES (%s) ON CONFLICT ({column}) DO NOTHING RETURNING id;"
            cur.execute(query, (value,))
            result_id = cur.fetchone()[0]
            return result_id
    except Exception as e:
        print(f"Error inserting into {table} '{value}': {e}")
    finally:
        conn.commit()
        cur.close()
        conn.close()

def insert_location(country):
    return insert_if_not_exists("locations", "country", country)

def link_keyword_to_job(keyword_id, job_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO job_keywords (keyword_id, job_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (keyword_id, job_id))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()


