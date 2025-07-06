from pydantic import BaseModel, Field
from typing import Annotated, Union, Literal
from enum import Enum


TaskIdType = Annotated[str, Field(min_length=16)]


class ExchangeIdentifier(Enum):
    OKX = "okx"


TaskStateType = Literal[
    "PENDING", "STARTED",
    "RETRY", "SUCCESS",
    "FAILURE", "REVOKED"
]


class TaskStatus(BaseModel):
    state: TaskStateType
    progress: Annotated[int, Field(gt=0, le=100)] | None
    task_id: TaskIdType


class TaskCreated(BaseModel):
    task_id: TaskIdType
