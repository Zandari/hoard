from pydantic import Field
from typing import Annotated
from datetime import datetime, timedelta
from .router import router
from .schema import (
    ExchangeIdentifier,
    TaskCreated,
    TaskStatus,
    TaskIdType
)
from app.tasks.historical import fetch_historical_data
from celery.result import AsyncResult


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
    task = fetch_historical_data.delay(
        exchange_identifier=exchange.value,
        instrument_identifier=instrument,
        start_dt=start_dt,
        end_dt=end_dt,
        period=period,
    )
    return TaskCreated(task_id=task.id)


@router.get('/task/{task_id}')
async def task_status(task_id: TaskIdType):
    task = AsyncResult(task_id)
    return TaskStatus(
        task_id=task.id,
        state=task.state,
        progress=None,
    )
    print(task.info)
