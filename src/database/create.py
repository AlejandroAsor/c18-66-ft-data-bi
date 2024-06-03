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
        """
        """
        CREATE TABLE IF NOT EXISTS job_keywords (
            keyword_id INTEGER REFERENCES keywords(id),
            job_id VARCHAR(255) NOT NULL,
            source_db_id INTEGER REFERENCES source_database(id),
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


def insert_keyword(keyword):
    conn = get_connection()  # Asegúrate de que esta función devuelve una conexión válida
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO keywords (keyword) VALUES (%s) ON CONFLICT (keyword) DO NOTHING RETURNING id;", (keyword,))
        keyword_id = cur.fetchone()
        if keyword_id:
            return keyword_id[0]
        return None
    except Exception as e:
        print(f"Error inserting keyword '{keyword}': {e}")
    finally:
        conn.commit()  # Asegúrate de confirmar la transacción
        cur.close()
        conn.close()


def link_keyword_to_job(keyword_id, job_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO job_keywords (keyword_id, job_id) VALUES (%s, %s);", (keyword_id, job_id))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()

