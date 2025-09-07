from app.crud.base import BaseDAO
from app.schemas.item import SItemFilter, SItemDocument
from app.core.config import settings


class ItemDAO(BaseDAO[SItemFilter, SItemDocument]):
    index_name = settings.INDEX_NAME
    filter_schema = SItemFilter
    pydantic_model = SItemDocument
