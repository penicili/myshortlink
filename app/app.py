from contextlib import asynccontextmanager
from secrets import token_urlsafe

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

try:
    from .database import get_db, init_db
except ImportError:
    from database import get_db, init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


class Link(BaseModel):
    link: str


# Health check
@app.get("/")
def healthcheck():
    return {"status": "OK"}


# Create shortlink
@app.post("/shorten")
def shorten_link(data: Link):

    # Generate random short code
    short_code = token_urlsafe(6)

    with get_db() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO links (short_code, original_url)
                VALUES (%s, %s)
                """,
                (short_code, data.link),
            )

    return {"original_link": data.link, "shortened_link": short_code}


# Open shortlink
@app.get("/{shortlink}")
def redirect(shortlink: str):

    with get_db() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT original_url
                FROM links
                WHERE short_code = %s
                """,
                (shortlink,),
            )

            result = cur.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Shortlink not found")

    return RedirectResponse(url=result[0])


# Delete shortlink
@app.delete("/{shortlink}")
def delete(shortlink: str):

    with get_db() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM links
                WHERE short_code = %s
                """,
                (shortlink,),
            )

            deleted = cur.rowcount

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Shortlink not found")

    return {"message": "Shortlink deleted", "shortlink": shortlink}
