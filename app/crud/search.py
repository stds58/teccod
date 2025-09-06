from app.crud.base import BaseDAO
from app.schemas.search import SSearchFilter, SSearchAdd, SSearchDocument
from app.core.config import settings


class ItemDAO(BaseDAO[SSearchAdd, SSearchFilter, SSearchDocument]):
    index_name = settings.INDEX_NAME
    create_schema = SSearchAdd
    filter_schema = SSearchFilter
    pydantic_model = SSearchDocument
