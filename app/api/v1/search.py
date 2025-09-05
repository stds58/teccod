from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search import search_documents
from fastapi.templating import Jinja2Templates



# pylint: disable=duplicate-code
V1_DIR = Path(__file__).resolve().parent
API_DIR = V1_DIR.parent
APP_DIR = API_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"
# pylint: enable=duplicate-code


router = APIRouter(tags=["Фронтенд"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# @router.post("/search", response_model=SearchResponse)
# def search_endpoint(request: SearchRequest):
#     try:
#         results = search_documents(query=request.query, content_type=request.content_type)
#         return SearchResponse(results=results)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")

# 🟩 Главная страница — отдаём HTML форму
@router.get("/")
def get_search_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 🟦 API: Поиск через GET (для формы)
@router.get("/search", response_model=SearchResponse)
def search_api(
    request: Request,
    q: str = Query(..., alias="q", description="Ключевое слово для поиска"),
    type: str = Query(None, alias="type", description="Фильтр по типу контента")
):
    """
    Обработка GET-запроса из формы.
    Параметры:
    - q: строка поиска
    - type: content_type (может быть пустым)
    """
    try:
        results = search_documents(query=q, content_type=type if type else None)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


