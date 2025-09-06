from app.db.opensearch_client import get_client
from app.core.config import settings
from typing import List
from app.schemas.search import SSearchFilter, SSearchAdd, SSearchDocument


def search_documents(filters: SSearchFilter) -> List[SSearchDocument]:
    """
    Ищет документы по title, content и content_type.
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

    search_body = {
        "query": {
            "bool": {
                "must": must_conditions
            }
        }
    }

    try:
        response = client.search(index=settings.INDEX_NAME, body=search_body)
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return []

    results = []
    hits = response.get("hits", {}).get("hits", [])

    for hit in hits:
        source = hit["_source"]
        # Создаем Pydantic-объект из сырых данных
        doc = SSearchDocument(
            id=hit.get("_id"),
            score=hit.get("_score"),
            title=source.get("title", ""),
            content=source.get("content", ""),
            content_type=source.get("content_type", "")
        )
        results.append(doc)

    return results
