from opensearchpy import OpenSearch
from fastapi import Depends
from app.core.config import settings


client = OpenSearch(
    hosts=[settings.OPENSEARCH_HOST],
    http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=False,
    timeout=30
)

def get_opensearch():
    return client
