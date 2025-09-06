import os
import time
import logging
from app.core.config import settings
from opensearchpy import exceptions
from app.db.opensearch_client import get_client
from opensearchpy.exceptions import ConnectionError, ConnectionTimeout


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_index(client):
    logger.info("Запуск инициализации OpenSearch...")
    if client.indices.exists(index=settings.INDEX_NAME):
        logger.info(f"Индекс '{settings.INDEX_NAME}' уже существует.")
        return

    logger.info(f"Создаю индекс '{settings.INDEX_NAME}'...")

    index_body = {
        "settings": {
            "index": {"number_of_shards": 1, "number_of_replicas": 0}
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "content_type": {"type": "keyword", "null_value": "unknown"}
            }
        }
    }

    try:
        response = client.indices.create(index=settings.INDEX_NAME, body=index_body)
        logger.info(f"Индекс создан: {response}")
    except exceptions.RequestError as e:
        logger.error(f"Ошибка при создании индекса: {e}")


if __name__ == "__main__":
    client = get_client()
    if client.success:
        create_index(client=client.credentials)
    else:
        logger.info("Бд недоступна.")
