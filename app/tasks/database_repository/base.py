from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from datetime import timedelta
import typing


class BaseRepository(ABC):
    @abstractmethod
    def insert_candlestick(
        self,
        exchange_identifier: str,
        instrument_identifier: str,
        period: timedelta | str,
        open_price: int | float,
        highest_price: int | float,
        lowest_price: int | float,
        close_price: int | float,
    ) -> None:
        ...

    @abstractmethod
    def __enter__(self) -> typing.Self: ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
