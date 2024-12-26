import os
import ssl

from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis
import requests


# Класс для управления настройками приложения через Pydantic
class Settings(BaseSettings):
    REDIS_PORT: int               # Порт для подключения к Redis       # Пароль для подключения к Redis
    BASE_URL: str                 # Базовый URL приложения
    REDIS_HOST: str               # Хост Redis-сервера
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Корневая директория проекта
    UPLOAD_DIR: str = os.path.join(BASE_DIR, 'app/uploads')
    # Указание файла с переменными окружения
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


# Создание экземпляра настроек
settings = Settings()

# # Опции для работы с SSL, отключаем проверку сертификата (подходит для отладки)
ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

redis_url = f"redis://redis:6379/0"
celery_app = Celery("celery_worker", broker=redis_url, backend=redis_url)


# celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

celery_app.conf.update(

    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,  # Убедитесь, что UTC включен
    timezone='Europe/Moscow',  # Устанавливаем московское время
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
redis_client = redis.Redis(host=settings.REDIS_HOST,
                           port=settings.REDIS_PORT,
                           db=0,
                           )

@celery_app.task(
    name='delete_file_scheduled',
    bind=True,
    max_retries=3,
    default_retry_delay=5
)
def delete_file_scheduled(self, file_id, dell_id):
    """Задача для отложенного удаления файла"""
    try:
        response = requests.delete(f"{settings.BASE_URL}/delete/{file_id}/{dell_id}")
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as exc:
        self.retry(exc=exc)
    except Exception as e:
        return None