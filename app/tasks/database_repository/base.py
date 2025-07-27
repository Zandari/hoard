from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from datetime import timedelta
import typing


class BaseRepository(ABC, AbstractContextManager):

    @abstractmethod
    @classmethod
    def from_url(cls) -> typing.Self:
        ...


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

    def __enter__(self) -> typing.Self:
        ...

    def __exit__(self) -> None:
        ...
