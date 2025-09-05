"""
Класс настроек приложения
"""

import os
from typing import List
from functools import lru_cache
from urllib.parse import urlparse
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))  # app/core/
parent_dir = os.path.dirname(current_dir)  # app/
project_dir = os.path.dirname(parent_dir)  # fastapi_template/
env_path = os.path.join(project_dir, ".env")


class Settings(BaseSettings):
    """
    берёт настройки из .env-а
    упадёт с ошибкой если в классе Settings не будет описана хотя бы одна настройка из .env-а
    """

    OPENSEARCH_INITIAL_ADMIN_PASSWORD: str
    OPENSEARCH_HOST: str
    OPENSEARCH_USER: str
    OPENSEARCH_PASSWORD: str
    INDEX_NAME: str
    CONTENT_TYPE_VALUESX: str

    @property
    def CONTENT_TYPE_VALUES(self) -> List[str]:  # pylint: disable=invalid-name
        return [item.strip() for item in settings.CONTENT_TYPE_VALUESX.split(",") if item.strip()]


    class Config:  # pylint: disable=too-few-public-methods
        extra = "ignore"



@lru_cache()
def get_settings():
    """
    кеширует экземпляр объекта настроек Settings, чтобы избежать повторной инициализации
    """
    return Settings()


settings = get_settings()
