import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def test_conexion_postgresql():
    """Verifica la conexión del sistema con PostgreSQL."""
    database_url = os.getenv("DATABASE_URL")

    assert database_url is not None, "DATABASE_URL no está configurado en el archivo .env"

    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    cur.execute("SELECT 1;")
    result = cur.fetchone()

    cur.close()
    conn.close()

    assert result[0] == 1