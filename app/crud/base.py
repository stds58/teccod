from app.db.opensearch_client import get_client
from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel as PydanticModel
from opensearchpy import OpenSearch



# pylint: disable-next=no-name-in-module,invalid-name
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticModel)
# pylint: disable-next=no-name-in-module,invalid-name
FilterSchemaType = TypeVar("FilterSchemaType", bound=PydanticModel)
# pylint: disable-next=no-name-in-module,invalid-name
PydanticModel = TypeVar("PydanticModel", bound=PydanticModel)

class BaseDAO(Generic[CreateSchemaType, FilterSchemaType]):
    index_name: str
    create_schema: type[CreateSchemaType]
    filter_schema: type[FilterSchemaType]
    pydantic_model: type[PydanticModel]

    @classmethod
    async def find_many(
            cls,
            client: OpenSearch,
            filters: Optional[FilterSchemaType] = None,
            size: int = 10,
            from_: int = 0,
    ) -> List[PydanticModel]:
        """
        Выполняет поиск по индексу с фильтрами.
        Возвращает список Pydantic-моделей.
        """
        # Базовый запрос
        query_body: Dict[str, Any] = {
            "query": {"match_all": {}},
            "size": size,
            "from": from_
        }

        # Применяем фильтры, если есть
        if filters is not None:
            query_body["query"] = cls._build_query(filters)

        # Выполняем поиск
        response = client.search(
            index=cls.index_name,
            body=query_body
        )

        # Извлекаем hits
        hits = response["hits"]["hits"]
        results = []

        for hit in hits:
            source = hit["_source"]
            # Валидируем и создаём Pydantic-объект
            obj = cls.pydantic_model.model_validate(source)  # Pydantic v2
            # Если Pydantic v1 — используйте: cls.pydantic_model.parse_obj(source)
            results.append(obj)

        return results

    @classmethod
    def _build_query(cls, filters: FilterSchemaType) -> Dict[str, Any]:
        """
        Строит OpenSearch-запрос на основе фильтров.
        Простая реализация — можно расширить под ваши нужды.
        """
        # Получаем поля фильтра как словарь
        filter_dict = filters.model_dump(exclude_none=True)  # или .dict(exclude_none=True) для v1

        if not filter_dict:
            return {"match_all": {}}

        # Пример: простой multi_match по нескольким полям
        # Можно заменить на bool + must/should/filter и т.д.
        fields = list(filter_dict.keys())
        query_value = " ".join(str(v) for v in filter_dict.values())

        return {
            "multi_match": {
                "query": query_value,
                "fields": fields,
                "type": "best_fields"
            }
        }


    @classmethod
    async def add_one(
            cls,
            client: OpenSearch,
            document: CreateSchemaType,
            doc_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Добавляет один документ в индекс OpenSearch.
        Возвращает ответ от OpenSearch (включая _id, _index и т.д.).
        """
        body = document.model_dump()  # или .dict() если Pydantic v1

        # Если нужно — можно добавить id документа
        response = client.index(
            index=cls.index_name,
            body=body,
            id=doc_id,
            refresh=True  # чтобы документ был сразу доступен для поиска
        )
        return response
