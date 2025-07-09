from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator
from math import ceil
from .common import CandlestickPeriod, Candlestick


class LiveDataClient(ABC):
    ...


class BaseMarketProvider(ABC):
    @abstractmethod
    def fetch_historical_market_data(
        self,
        instrument: str,
        start: datetime,
        end: datetime,
        candlestick_period: CandlestickPeriod,
    ) -> Generator[Candlestick, None, None]:
        ...

    @staticmethod
    def get_estimated_candlestick_amount(
        start: datetime,
        end: datetime,
        candlestick_period: CandlestickPeriod,
    ) -> int:
        return ceil((end - start) / candlestick_period.value.delta)

    @abstractmethod
    def get_live_data_client(self) -> LiveDataClient:
        ...
