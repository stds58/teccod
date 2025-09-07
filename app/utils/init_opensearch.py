import logging
from opensearchpy import exceptions
from app.core.config import settings
from app.db.opensearch_client import get_client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_index(client):
    logger.info("Запуск инициализации OpenSearch...")
    if client.indices.exists(index=settings.INDEX_NAME):
        logger.info("Индекс '%s' уже существует.", settings.INDEX_NAME)
        return

    logger.info("Создаю индекс '%s'...", settings.INDEX_NAME)

    index_body = {
        "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "content_type": {"type": "keyword", "null_value": "unknown"},
            }
        },
    }

    try:
        response = client.indices.create(index=settings.INDEX_NAME, body=index_body)
        logger.info("Индекс создан: %s", response)
    except exceptions.RequestError as e:
        logger.error("Ошибка при создании индекса: %s", e)


if __name__ == "__main__":
    opensearch_client = get_client()
    if opensearch_client.success:
        create_index(client=opensearch_client.credentials)
    else:
        logger.info("Бд недоступна.")
