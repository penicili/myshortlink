import os
import time
from urllib.parse import urlparse

import psycopg
from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECT_RETRIES = int(os.getenv("DB_CONNECT_RETRIES", "15"))
DB_CONNECT_DELAY = float(os.getenv("DB_CONNECT_DELAY", "1"))


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


def _connect_with_retry(dbname: str, autocommit: bool = False):
    last_error = None

    for _ in range(DB_CONNECT_RETRIES):
        try:
            host, port = _resolve_host_port()
            return psycopg.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=DB_USER,
                password=DB_PASSWORD,
                autocommit=autocommit,
            )
        except psycopg.OperationalError as err:
            last_error = err
            time.sleep(DB_CONNECT_DELAY)

    if last_error is not None:
        raise last_error

    raise RuntimeError("Database connection failed without explicit error")


def init_db():
    # CREATE DATABASE must run with autocommit enabled.
    with _connect_with_retry("postgres", autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1
                FROM pg_database
                WHERE datname = 'mydb'
                """)

            if cur.fetchone() is None:
                cur.execute("CREATE DATABASE mydb")

    # Connect to mydb and create tables
    with _connect_with_retry("mydb") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id SERIAL PRIMARY KEY,
                    short_code VARCHAR(10) UNIQUE NOT NULL,
                    original_url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
