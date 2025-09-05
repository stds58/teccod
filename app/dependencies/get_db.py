from fastapi import Depends
from app.db.opensearch_client import client

def get_opensearch():
    """
    Зависимость для внедрения клиента OpenSearch
    """
    return client
