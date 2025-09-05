import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from opensearchpy import OpenSearch
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Настройки OpenSearch
OPENSEARCH_HOST = "https://localhost:9200/" #os.getenv("OPENSEARCH_HOST")
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USER")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD")


# Подключение
client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
    timeout=30
)

INDEX_NAME = "documents"
CONTENT_TYPES = ["article", "blog", "news", "tutorial"]

# Создание индекса
def create_index():
    if client.indices.exists(index=INDEX_NAME):
        client.indices.delete(index=INDEX_NAME)

    body = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "content_type": {"type": "keyword"}
            }
        }
    }
    client.indices.create(index=INDEX_NAME, body=body)
    print("✅ Индекс создан")

# Загрузка тестовых данных
def load_data():
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
        client.index(index=INDEX_NAME, body=doc, refresh=True)
        print(f"📥 Добавлен: {doc['title']} [{doc['content_type']}]")

# Поиск
def search(keyword, content_type=None):
    query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["title", "content"]
                }
            },
            "filter": []
        }
    }

    if content_type and content_type in CONTENT_TYPES:
        query["bool"]["filter"].append({"term": {"content_type": content_type}})

    try:
        response = client.search(index=INDEX_NAME, body={"query": query}, size=10)
        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            snippet = (source["content"][:50] + "...") if len(source["content"]) > 50 else source["content"]
            results.append({
                "title": source["title"],
                "snippet": snippet
            })
        return results
    except Exception as e:
        print("Ошибка поиска:", e)
        return []

# Веб-сервер (без фреймворков)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Определяем путь к файлу относительно расположения app.py
            file_path = os.path.join(os.path.dirname(__file__), "index.html")
            print('file_path  ',file_path)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            except FileNotFoundError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"<h1> error: index.html not found</h1>")
                return

        elif parsed.path == "/search":
            query = parse_qs(parsed.query)
            keyword = query.get("q", [""])[0].strip()
            content_type = query.get("type", [""])[0]

            if not keyword:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "empty query"}).encode())
                return

            results = search(keyword, content_type)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results, ensure_ascii=False, indent=2).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

# Запуск
if __name__ == "__main__":
    # Ждём OpenSearch
    for _ in range(15):
        try:
            if client.ping():
                print("🟢 Подключено к OpenSearch")
                break
        except Exception as e:
            print("🟡 Ожидание OpenSearch...", e)
            time.sleep(5)
    else:
        print("🔴 Не удалось подключиться")
        exit(1)

    create_index()
    load_data()

    # Запуск веб-сервера
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("🌐 Сервер запущен на http://localhost:8000")
    server.serve_forever()


