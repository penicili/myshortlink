from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Health check
@app.get('/')
def healthcheck():
    return {'OK'}

# Shorten link
@app.post('/')
def shorten_link(link):
    return {"Shortened Link"}

# Open shortlink
@app.get('/{shortlink}')
def redirect(shortlink):
    return {"Redirect to link"}

# Deletes
@app.delete('/{shortlink}')
def delete(shortlink):
    # Cek apakah dia yang buat
    if (True):
        return {"Shortlink deleted"}
    else:
        return {"No you don't"}