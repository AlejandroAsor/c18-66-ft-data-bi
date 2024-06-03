from src.database.connection import get_connection
def fetch_job_ids_by_keyword(keyword):
    conn = get_connection(db_type="keywords")
    cur = conn.cursor()
    cur.execute("SELECT id FROM keywords WHERE keyword = %s;", (keyword,))
    keyword_id = cur.fetchone()
    if keyword_id:
        keyword_id = keyword_id[0]
        cur.execute("SELECT job_id FROM job_keywords WHERE keyword_id = %s;", (keyword_id,))
        job_ids = cur.fetchall()
        conn.close()
        return [job_id[0] for job_id in job_ids]
    return []


def fetch_job_details(job_ids):
    conn = get_connection(db_type="computrabajo")
    cur = conn.cursor()
    query = "SELECT * FROM job_listings WHERE id = ANY(%s);"
    cur.execute(query, (job_ids,))
    job_details = cur.fetchall()
    return job_details


if __name__ == "__main__":
    job_ids = fetch_job_ids_by_keyword("java")
    if job_ids:
        job_details = fetch_job_details(job_ids)
        for job in job_details:
            print(job)
    else:
        print("No se encontraron trabajos asociados con la palabra clave 'Python'")
