from app.db.opensearch_client import client
from app.core.config import settings
from typing import List
from app.schemas.search import SearchResponseItem


def search_documents(query: str, content_type: str = None) -> List[SearchResponseItem]:
    """
    Ищет документы по ключевому слову в title и content.
    Фильтрует по content_type, если указан.
    Возвращает title и snippet (первые 50 символов content).
    """
    # Формируем тело запроса
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "content"],
                            "type": "best_fields"
                        }
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "content": {"fragment_size": 50, "number_of_fragments": 1}
            }
        }
    }
    print('=======================')

    # Добавляем фильтр по content_type, если указан
    if content_type:
        search_body["query"]["bool"]["filter"] = [
            {"term": {"content_type": content_type}}
        ]

    try:
        response = client.search(index=settings.INDEX_NAME, body=search_body)
        print('response ',response)
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return []

    results = []
    for hit in response["hits"]["hits"]:
        title = hit["_source"]["title"]
        # Используем highlight, если есть; иначе — обрезаем content
        if "highlight" in hit and "content" in hit["highlight"]:
            snippet = hit["highlight"]["content"][0]
        else:
            content = hit["_source"]["content"]
            snippet = content[:50] + "..." if len(content) > 50 else content
        results.append(SearchResponseItem(title=title, snippet=snippet))

    return results
