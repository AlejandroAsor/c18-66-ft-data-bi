from src.database.connection import get_connection

def fetch_and_store_keyword_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT k.keyword, COUNT(jk.job_id) AS job_count
    FROM keywords k
    LEFT JOIN job_keywords jk ON k.id = jk.keyword_id
    GROUP BY k.keyword
    ORDER BY job_count DESC;
    """)
    results = cur.fetchall()

    print("Keyword - Job Count")
    for row in results:
        print(f"{row[0]} - {row[1]}")

    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS keyword_counts
        (
            keyword TEXT NOT NULL,
            job_count INTEGER NOT NULL
        );
        """)
        cur.execute("DELETE FROM keyword_counts;")
        for row in results:
            cur.execute("INSERT INTO keyword_counts (keyword, job_count) VALUES (%s, %s);", (row[0], row[1]))
        conn.commit()
        print("Datos insertados correctamente en la tabla keyword_counts.")
    except Exception as e:
        print(f"Error al insertar datos en keyword_counts: {e}")
        conn.rollback()

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    fetch_and_store_keyword_counts()
