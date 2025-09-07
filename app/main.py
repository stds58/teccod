from pathlib import Path
from fastapi import FastAPI, Response, status, Request
from fastapi.templating import Jinja2Templates
from app.api.v1.base_router import v1_router


app = FastAPI(
    title="OpenSearch Search API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(v1_router, prefix="/api")

# pylint: disable=duplicate-code
APP_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = APP_DIR / "templates"
# pylint: enable=duplicate-code
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health_check")
async def health_check():
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000)
