from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncGenerator
from .common import CandlestickPeriod


class LiveDataClient(ABC):
    ...


class BaseMarketProvider(ABC):
    @abstractmethod
    async def fetch_historical_market_data(
        self,
        instrument: str,
        start: datetime,
        end: datetime,
        candlestick_period: CandlestickPeriod,
    ) -> AsyncGenerator:
        ...

    @abstractmethod
    def get_live_data_client(self) -> LiveDataClient:
        ...
