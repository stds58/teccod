from fastapi import FastAPI, Response, status
from app.api.v1.base_router import v1_router


app = FastAPI(title="OpenSearch Search API")

app.include_router(v1_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "FastAPI + OpenSearch. Use /search to query."}


@app.get("/health_check")
async def health_check():
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    # uvicorn.run("main:app", reload=False)
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
    # python -m cProfile -o output.prof -m uvicorn app.main:app
    # В боевом режиме лучше использовать Gunicorn + Uvicorn workers вместо uvicorn.run(...)
    # https://webadventures.ru/sravnenie-wsgi-serverov-uvicorn-i-gunicorn/
