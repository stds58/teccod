from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from app.schemas.search import SSearchFilter, SSearchAdd, SSearchDocument
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


@router.get("/search", response_model=list[SSearchDocument], summary="Поиск документов")
def api_search(filters: SSearchFilter = Depends()):
    """
    Выполняет поиск документов в OpenSearch.
    Можно фильтровать по title, content и content_type.
    """
    results = search_documents(filters=filters)
    return results


# @router.post("", summary="Create order nanny for young")
# async def create_nanny(request: Request, data: SFormFields, session: AsyncSession = Depends(connection())):
#     row = await add_one_search(request=request, data=data, session=session)
#     return {"data": row}

