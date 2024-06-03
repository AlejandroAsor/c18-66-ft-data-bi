import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import DatabaseError
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

def create_database(conn, dbname):
    """Intenta crear la base de datos si no existe utilizando la conexión dada."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {dbname};")
        cursor.close()
        print(f"Base de datos {dbname} creada exitosamente.")
    except DatabaseError as e:
        print(f"No se pudo crear la base de datos {dbname}: {e}")
        cursor.close()

def get_connection(db_type="keywords"):
    """Crea y retorna una conexión a la base de datos especificada por `db_type`, creándola si no existe."""
    if db_type == "keywords":
        dbname = os.getenv("KEYWORDS_DB_NAME")
        user = os.getenv("KEYWORDS_DB_USER")
        password = os.getenv("KEYWORDS_DB_PASSWORD")
        host = os.getenv("KEYWORDS_DB_HOST")
        port = os.getenv("KEYWORDS_DB_PORT")
    elif db_type == "computrabajo":
        dbname = os.getenv("COMP_DB_NAME")
        user = os.getenv("COMP_DB_USER")
        password = os.getenv("COMP_DB_PASSWORD")
        host = os.getenv("COMP_DB_HOST")
        port = os.getenv("COMP_DB_PORT")
    elif db_type == "elempleo":
        dbname = os.getenv("ELEMPL_DB_NAME")
        user = os.getenv("ELEMPL_DB_USER")
        password = os.getenv("ELEMPL_DB_PASSWORD")
        host = os.getenv("ELEMPL_DB_HOST")
        port = os.getenv("ELEMPL_DB_PORT")
    else:
        raise ValueError("Tipo de base de datos no soportado.")

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.OperationalError:
        print(f"La base de datos {dbname} no existe. Intentando crearla...")
        # Intenta conectarte a la base de datos por defecto (postgres) para crear la nueva base de datos
        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_database(conn, dbname)
        conn.close()
        # Intenta reconectar a la nueva base de datos
        return get_connection(db_type)

if __name__ == "__main__":
    # Test de la conexión a la base de datos de keywords
    conn_keywords = get_connection("keywords")
    if conn_keywords:
        print("Conexión a 'keywords' establecida correctamente.")
        conn_keywords.close()

    # Test de la conexión a la base de datos de computrabajo
    conn_computrabajo = get_connection("computrabajo")
    if conn_computrabajo:
        print("Conexión a 'computrabajo' establecida correctamente.")
        conn_computrabajo.close()
