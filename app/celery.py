from celery import Celery


celery_app = Celery(
    "hoard",
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)


from app.tasks.historical import *
