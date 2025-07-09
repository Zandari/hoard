from pydantic import Field
from typing import Annotated
from datetime import datetime
from .router import router
from .schema import (
    ExchangeIdentifier,
    TaskCreated,
    TaskStatus,
    TaskStatusProgress,
    TaskStatusErrorDescription,
    TaskIdType,
)
from app.tasks.historical import fetch_historical_data_task
from app.tasks.data_providers.exceptions import FetchingError
from celery.result import AsyncResult
from app.celery import celery_app


@router.post(
    path='/task',
    response_model=TaskCreated,
    status_code=201,
)
async def create_fetch_task(
    exchange: ExchangeIdentifier,
    instrument: Annotated[str, Field(max_length=32, alias='inst')],
    start_dt: Annotated[datetime, Field(alias='start')],
    end_dt: Annotated[datetime, Field(alias='end')],
    period: str,
):
    task = fetch_historical_data_task.delay(
        exchange_identifier=exchange.value,
        instrument_identifier=instrument,
        start_dt=start_dt,
        end_dt=end_dt,
        period=period,
    )
    return TaskCreated(task_id=task.id)


@router.get(
    path='/task/{task_id}',
    response_model=TaskStatus
)
async def task_status(task_id: TaskIdType):
    task = AsyncResult(task_id)

    data = None
    if task.state == "PROGRESS":
        data = TaskStatusProgress(**task.result)
    elif task.state == "FAILURE":
        exc = task.result
        if isinstance(exc, FetchingError):
            data = TaskStatusErrorDescription(
                code=exc.code,
                message=exc.message,
            )
        else:
            data = TaskStatusErrorDescription(
                code=-1,
                message="Unexpected error occured while executiong hoard task."
            )

    return TaskStatus(
        task_id=task.id,
        state=task.state,
        data=data
    )
