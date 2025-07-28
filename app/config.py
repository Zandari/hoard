import os


class Config:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379/1')
    DATABASE_URL = os.getenv('DATABASE_URL', 'quest://admin:quest@localhost:9000')
    MARKET_DATA_TABLE_NAME = os.getenv('MARKET_DATA_TABLE_NAME', 'market_data')
