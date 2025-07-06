from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import historical_hoard_control_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.celery import celery_app
    worker = celery_app.Worker()
    worker.start()
    yield
    worker.stop()
    celery_app.close()


app = FastAPI(lifespan=lifespan)
app.include_router(historical_hoard_control_router, prefix='/historical')
