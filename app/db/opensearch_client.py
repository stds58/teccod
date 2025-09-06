import logging
from fastapi import Depends
from app.core.config import settings
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.exceptions import ConnectionError, ConnectionTimeout
from dataclasses import dataclass



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HealthCheckResult:
    success: bool
    reason: str
    details: str = ""
    credentials: str = ""


def check_opensearch_healthy(client, timeout=30.0):
    try:
        health = client.cluster.health(wait_for_status="yellow", timeout=timeout)
        status = health["status"]
        print(f"Health status: {status}")
        if status in ("green", "yellow"):
            logger.info(f"Кластер готов. Статус: {status}")
            return HealthCheckResult(success=True, reason="OK")
        else:
            msg = f"Кластер в состоянии {status}"
            logger.error(msg)
            return HealthCheckResult(success=False, reason="UNHEALTHY", details=msg)
    except (ConnectionError, ConnectionTimeout) as e:
        msg = f"Нет соединения: {type(e).__name__}: {e}"
        logger.error(msg)
        return HealthCheckResult(success=False, reason="UNREACHABLE", details=msg)
    except ValueError as e:
        msg = f"Невалидный ответ: {e}"
        logger.error(msg)
        return HealthCheckResult(success=False, reason="INVALID_RESPONSE", details=msg)
    except Exception as e:
        msg = f"Неизвестная ошибка: {type(e).__name__}: {e}"
        logger.error(msg)
        return HealthCheckResult(success=False, reason="UNKNOWN_ERROR", details=msg)


def get_client():
    credentials = OpenSearch(
        hosts=[settings.OPENSEARCH_HOST],
        http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
        connection_class=RequestsHttpConnection,
        timeout=30
    )
    health_check = check_opensearch_healthy(client=credentials)
    if health_check.success:
        health_check.credentials = credentials
    return health_check
