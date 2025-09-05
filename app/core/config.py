"""
Класс настроек приложения
"""

import os
from functools import lru_cache
from urllib.parse import urlparse
# from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))  # app/core/
parent_dir = os.path.dirname(current_dir)  # app/
project_dir = os.path.dirname(parent_dir)  # fastapi_template/
env_path = os.path.join(project_dir, ".env")


def prepare_env_values(env_values: dict) -> dict:
    return {k: v for k, v in env_values.items() if isinstance(v, str)}


def expand_template(template: str, env_values: dict) -> str:
    """Заменяет ${VAR} на значения из словаря, только если значение — строка"""
    for key, value in env_values.items():
        if isinstance(value, str):
            template = template.replace(f"${{{key}}}", value)
    return template


class Settings(BaseSettings):
    """
    берёт настройки из .env-а
    упадёт с ошибкой если в классе Settings не будет описана хотя бы одна настройка из .env-а
    """

    OPENSEARCH_INITIAL_ADMIN_PASSWORD: str
    OPENSEARCH_HOST: str
    OPENSEARCH_USER: str
    OPENSEARCH_PASSWORD: str


    class Config:  # pylint: disable=too-few-public-methods
        extra = "ignore"


@lru_cache()
def get_settings():
    """
    кеширует экземпляр объекта настроек Settings, чтобы избежать повторной инициализации
    """
    return Settings()


settings = get_settings()