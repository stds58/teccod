import os
import time
import logging
from app.core.config import settings
from opensearchpy import exceptions
from app.db.opensearch_client import client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_index():
    """Создаёт индекс с нужной схемой, если его ещё нет."""
    if client.indices.exists(index=settings.INDEX_NAME):
        logger.info(f"Индекс '{settings.INDEX_NAME}' уже существует.")
        return

    logger.info(f"Создаю индекс '{settings.INDEX_NAME}'...")

    index_body = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "content_type": {
                    "type": "keyword",
                    "null_value": "unknown"
                }
            }
        }
    }

    try:
        response = client.indices.create(index=settings.INDEX_NAME, body=index_body)
        logger.info(f"Индекс создан: {response}")
    except exceptions.RequestError as e:
        if e.error == "resource_already_exists_exception":
            logger.info("Индекс уже был создан другой процессом.")
        else:
            logger.error(f"Ошибка при создании индекса: {e}")
            raise


def wait_for_opensearch():
    """Ждём, пока OpenSearch станет доступен."""
    for i in range(60):  # максимум 60 попыток
        try:
            if client.ping():
                logger.info("Подключение к OpenSearch установлено.")
                return
        except Exception as e:
            logger.warning(f"OpenSearch ещё не готов: {e}")
            time.sleep(5)
    raise RuntimeError("Не удалось подключиться к OpenSearch за отведённое время.")


if __name__ == "__main__":
    logger.info("Запуск инициализации OpenSearch...")
    wait_for_opensearch()
    create_index()
    logger.info("Инициализация завершена.")
