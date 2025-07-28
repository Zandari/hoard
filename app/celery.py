from celery import Celery
from app.config import Config


celery_app = Celery(
    "hoard",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_BACKEND_URL,
)


from app.tasks.historical import *
