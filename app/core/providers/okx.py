from math import ceil, floor
import aiohttp
import typing
from datetime import datetime
from .common import CandlestickPeriod, Candlestick
from .base import BaseMarketProvider


class OKXMarketProvider(BaseMarketProvider):
    def _get_session(self) -> ...:
        return aiohttp.ClientSession()

    async def fetch_historical_market_data(
        self,
        instrument: str,
        start: datetime,
        end: datetime,
        candlestick_period: CandlestickPeriod
    ) -> typing.AsyncIterator[Candlestick]:
        ENDPOINT = "https://us.okx.com/api/v5/market/history-index-candles"
        REQ_LIMIT = 300 # candles per request (max: 300)

        req_parameters = {
            "instId": instrument,
            "bar": str(candlestick_period.value),
            "limit": REQ_LIMIT
        }

        candlesticks_expected = int((end - start) / candlestick_period.value.delta)
        candlesticks_recieved = 0

        delta_per_request = REQ_LIMIT * candlestick_period.value.delta
        for index in range(ceil((end - start) / delta_per_request)):
            start_dt = start + index * delta_per_request
            req_parameters["before"] = self._datetime_to_timestamp_ms(start_dt)

            print(candlesticks_recieved)
            if (diff := candlesticks_expected - candlesticks_recieved) < REQ_LIMIT:
                end_dt = start_dt + diff * candlestick_period.value.delta
            else:
                end_dt = start_dt + delta_per_request
            req_parameters["after"] = self._datetime_to_timestamp_ms(end_dt)

            session = self._get_session()
            async with session.get(ENDPOINT, params=req_parameters) as response:
                response_json: dict = await response.json()
            await session.close()

            # TODO: assert resp code
            candlesticks_recieved += len(response_json['data'])
            for candlestick_data in response_json['data']:
                yield self._construct_candlestick(candlestick_data)


    def _datetime_to_timestamp_ms(self, dt: datetime) -> int:
        return int(dt.timestamp() * 1000)

    def _construct_candlestick(self, data: typing.Iterable[typing.Any]) -> Candlestick:
        corresponding_types: tuple[type] = (int, float, float, float, float)
        converted_values = [t(e) for t,e in zip(corresponding_types, data)]

        return Candlestick(*converted_values)

    def get_live_data_client(self) -> ...: ...
