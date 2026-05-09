import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def test_pgvector_instalado():
    """Verifica que pgvector esté instalado en la base de datos."""
    database_url = os.getenv("DATABASE_URL")

    assert database_url is not None, "DATABASE_URL no está configurado en el archivo .env"

    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
    result = cur.fetchone()

    cur.close()
    conn.close()

    assert result is not None, "La extensión pgvector no está instalada"
    assert result[0] == "vector"