import os
import ssl

from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict


# Класс для управления настройками приложения через Pydantic
class Settings(BaseSettings):
    REDIS_PORT: int               # Порт для подключения к Redis
    REDIS_PASSWORD: str           # Пароль для подключения к Redis
    BASE_URL: str                 # Базовый URL приложения
    REDIS_HOST: str               # Хост Redis-сервера
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Корневая директория проекта

    # Указание файла с переменными окружения
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


# Создание экземпляра настроек
settings = Settings()

# Формирование URL для подключения к Redis через SSL
redis_url = f"rediss://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

# Опции для работы с SSL, отключаем проверку сертификата (подходит для отладки)
ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

# Инициализация экземпляра Celery
celery_app = Celery(
    "celery_worker",  # Имя приложения Celery
    broker=redis_url,  # URL брокера задач (Redis)
    backend=redis_url  # URL для хранения результатов выполнения задач
)