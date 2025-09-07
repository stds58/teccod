from fastapi import APIRouter
from app.api.v1.item import router as search_router


v1_router = APIRouter()

v1_router.include_router(search_router, tags=["search"])
