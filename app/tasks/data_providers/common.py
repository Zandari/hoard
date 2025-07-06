from enum import Enum
from typing import NamedTuple
from datetime import timedelta


class Candlestick(NamedTuple):
    timestamp_ms: int
    open_price: float
    highest_price: float
    lowest_price: float
    close_price: float


class _Period(NamedTuple):
    id: str
    delta: timedelta

    def __str__(self) -> str:
        return self.id


class CandlestickPeriod(Enum):
    P1S = _Period("1s", timedelta(seconds=1))
    P1M = _Period("1m", timedelta(minutes=1))
    P3M = _Period("3m", timedelta(minutes=3))
    P5M = _Period("5m", timedelta(minutes=5))
    P15M = _Period("15m", timedelta(minutes=15))
    P30M = _Period("30m", timedelta(minutes=30))
    P1H = _Period("1H", timedelta(hours=1))
    P2H = _Period("2H", timedelta(hours=2))
    P4H = _Period("4H", timedelta(hours=4))
