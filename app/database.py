import os
from urllib.parse import urlparse

import psycopg
from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def _resolve_host_port() -> tuple[str, int]:
    # Support either DB_HOST + DB_PORT or DB_HOST="host:port"/URL style values.
    if "://" in DB_HOST:
        parsed = urlparse(DB_HOST)
        return (parsed.hostname or "localhost", parsed.port or DB_PORT)

    if ":" in DB_HOST:
        host, raw_port = DB_HOST.rsplit(":", 1)
        return (host, int(raw_port))

    return (DB_HOST, DB_PORT)


def get_db(dbname="mydb"):
    host, port = _resolve_host_port()
    return psycopg.connect(
        host=host, port=port, dbname=dbname, user=DB_USER, password=DB_PASSWORD
    )


def init_db():
    # CREATE DATABASE must run with autocommit enabled.
    host, port = _resolve_host_port()
    with psycopg.connect(
        host=host,
        port=port,
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1
                FROM pg_database
                WHERE datname = 'mydb'
                """)

            if cur.fetchone() is None:
                cur.execute("CREATE DATABASE mydb")

    # Connect to mydb and create tables
    with get_db("mydb") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id SERIAL PRIMARY KEY,
                    short_code VARCHAR(10) UNIQUE NOT NULL,
                    original_url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
