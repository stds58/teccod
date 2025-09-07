from fastapi import APIRouter, Depends
from app.schemas.item import SItemFilter, SItemDocument
from app.services.item import find_many_item


router = APIRouter(tags=["API"])


@router.get("/search", response_model=list[SItemDocument], summary="Поиск документов")
def api_search(filters: SItemFilter = Depends()):
    results = find_many_item(filters=filters)
    return results
