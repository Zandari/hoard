from pydantic import BaseModel, Field
from typing import Annotated, Union, Literal
from enum import Enum


TaskIdType = Annotated[str, Field(min_length=16)]


class ExchangeIdentifier(str, Enum):
    OKX = "okx"

    @classmethod
    def _missing_(cls, value):
        value_lower = value.lower()
        for member in cls:
            if member.value.lower() == value_lower:
                return member

        return None


TaskStateType = Literal[
    "PENDING", "STARTED",
    "RETRY", "SUCCESS",
    "FAILURE", "REVOKED",
    "PROGRESS"
]


class TaskStatusProgress(BaseModel):
    total: int
    completed: int


class TaskStatusErrorDescription(BaseModel):
    code: int | str
    message: str


class TaskStatus(BaseModel):
    task_id: TaskIdType
    state: TaskStateType
    data: TaskStatusProgress | TaskStatusErrorDescription | None


class TaskStatusCollection(BaseModel):
    data: list[TaskStatus]


class TaskCreated(BaseModel):
    task_id: TaskIdType
