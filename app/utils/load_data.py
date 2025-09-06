import logging
from app.core.config import settings
from app.db.opensearch_client import get_client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(client):
    logger.info("загрузка данных")
    index_name = settings.INDEX_NAME

    logger.info("Проверяем, существует ли индекс")
    if not client.indices.exists(index=index_name):
        logger.warning(f"Индекс '{index_name}' не существует. Пропускаем загрузку данных.")
        return

    logger.info("Проверяем, есть ли уже документы в индексе")
    response = client.count(index=index_name)
    doc_count = response.get("count", 0)
    if doc_count > 0:
        logger.info(f"В индексе '{index_name}' уже есть {doc_count} документов. Пропускаем загрузку.")
        return

    logger.info(f"Загружаю начальные данные в индекс '{index_name}'...")

    docs = [
        {
            "title": "Как выучить Python",
            "content": "Python — мощный язык. Начни с переменных, циклов и функций.",
            "content_type": "tutorial"
        },
        {
            "title": "Docker для начинающих",
            "content": "Docker упрощает деплой. Контейнеры — это будущее.",
            "content_type": "blog"
        },
        {
            "title": "OpenSearch vs Elasticsearch",
            "content": "OpenSearch — форк Elasticsearch от AWS. Полностью open-source.",
            "content_type": "article"
        },
        {
            "title": "Новости технологий",
            "content": "Сегодня анонсированы новые процессоры с ускорением ИИ.",
            "content_type": "news"
        },
        {
            "title": "Машинное обучение без математики",
            "content": "Scikit-learn позволяет использовать ML без глубоких знаний математики.",
            "content_type": "tutorial"
        }
    ]

    for doc in docs:
        client.index(index=settings.INDEX_NAME, body=doc, refresh=True)
        logger.info(f"Добавлен: {doc['title']} [{doc['content_type']}]")

    logger.info("Загрузка данных завершена.")


if __name__ == "__main__":
    client = get_client()
    if client.success:
        load_data(client=client.credentials)
    else:
        logger.info("Бд недоступна.")
