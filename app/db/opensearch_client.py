from fastapi import Depends
from app.core.config import settings
from opensearchpy import OpenSearch, RequestsHttpConnection


client = OpenSearch(
    hosts=[settings.OPENSEARCH_HOST],
    http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
    connection_class=RequestsHttpConnection,
    timeout=30
)

def get_opensearch():
    return client
