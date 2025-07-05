from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.historical.router import router as historical_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.celery import celery_app
    worker = celery_app.Worker()
    worker.start()
    yield
    #TODO worker.stop
    celery_app.close()


app = FastAPI(lifespan=lifespan)
app.include_router(historical_router, prefix='/historical')
