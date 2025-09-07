import logging
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel as PydanticModel
from app.core.config import settings
from app.db.opensearch_client import get_client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable-next=no-name-in-module,invalid-name
FilterSchemaType = TypeVar("FilterSchemaType", bound=PydanticModel)
# pylint: disable-next=no-name-in-module,invalid-name
ModelType = TypeVar("ModelType", bound=PydanticModel)


class BaseDAO(Generic[FilterSchemaType, ModelType]):
    index_name: str
    filter_schema: type[FilterSchemaType]
    pydantic_model: type[ModelType]

    @classmethod
    def find_many(cls, filters: Optional[FilterSchemaType] = None) -> List[ModelType]:
        """
        Выполняет поиск по индексу с фильтрами.
        Возвращает список Pydantic-моделей.
        """
        client = get_client().credentials
        must_conditions = []

        if filters.title:
            must_conditions.append({"match": {"title": filters.title}})

        if filters.content:
            must_conditions.append({"match": {"content": filters.content}})

        if filters.content_type:
            must_conditions.append({"match": {"content_type": filters.content_type}})

        if not must_conditions:
            must_conditions.append({"match_all": {}})

        search_body = {"query": {"bool": {"must": must_conditions}}}

        try:
            response = client.search(index=settings.INDEX_NAME, body=search_body)
        except Exception as e:
            logger.error("Ошибка поиска: %s", e)
            return []

        results = []
        hits = response.get("hits", {}).get("hits", [])

        for hit in hits:
            source = hit["_source"]
            try:
                doc = cls.pydantic_model(
                    id=hit.get("_id"),
                    score=hit.get("_score"),
                    **source,  # распаковываем остальные поля из source
                )
                results.append(doc)
            except Exception as e:
                logger.error(
                    "Ошибка создания модели %s: %s", cls.pydantic_model.__name__, e
                )
                continue

        return results
