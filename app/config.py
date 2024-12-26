import os
import ssl

from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict


# # Класс для управления настройками приложения через Pydantic
# class Settings(BaseSettings):
#     REDIS_PORT: int               # Порт для подключения к Redis
#     REDIS_PASSWORD: str           # Пароль для подключения к Redis
#     BASE_URL: str                 # Базовый URL приложения
#     REDIS_HOST: str               # Хост Redis-сервера
#     BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Корневая директория проекта

#     # Указание файла с переменными окружения
#     model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


# # Создание экземпляра настроек
# settings = Settings()

# # Формирование URL для подключения к Redis через SSL
# redis_url = f"rediss://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

# # Опции для работы с SSL, отключаем проверку сертификата (подходит для отладки)
# ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

# Создание экземпляра Celery
celery_app = Celery(
    "tasks",
    # broker="redis://localhost:6379/0",  # Брокер
    # backend="redis://localhost:6379/1",
)

celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)