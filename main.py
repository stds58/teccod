from fastapi import FastAPI
from .routes import search


app = FastAPI()

app.include_router(search.router, prefix="/api")

@app.get("/")
def health():
    return {"status": "ok"}
