import typing
import httpx
from time import sleep
from math import ceil
from datetime import datetime
from .common import CandlestickPeriod, Candlestick
from .base import BaseMarketProvider
from .exceptions import FetchingError


class OKXMarketProvider(BaseMarketProvider):
    TIMEOUT = 30
    RETRY_LIMIT = 3
    RETRY_TIMEOUT = 5


    def _get_http_client(self) -> httpx.Client:
        return httpx.Client()

    def fetch_historical_market_data(
        self,
        instrument: str,
        start: datetime,
        end: datetime,
        candlestick_period: CandlestickPeriod
    ) -> typing.Generator[Candlestick, None, None]:
        # raises FetchingError, httpx.HTTPError, JSONDecodeError, KeyError

        ENDPOINT = "https://us.okx.com/api/v5/market/history-index-candles"
        REQ_LIMIT = 300 # candles per request (max: 300)

        req_parameters = {
            "instId": instrument,
            "bar": candlestick_period.value.id,
            "limit": REQ_LIMIT
        }

        candlesticks_expected = self.get_estimated_candlestick_amount(
            start=start,
            end=end,
            candlestick_period=candlestick_period,
        )
        candlesticks_recieved = 0

        delta_per_request = REQ_LIMIT * candlestick_period.value.delta

        for index in range(ceil((end - start) / delta_per_request)):
            start_dt = start + index * delta_per_request
            req_parameters["before"] = self._datetime_to_timestamp_ms(start_dt)

            if (diff := candlesticks_expected - candlesticks_recieved) < REQ_LIMIT:
                end_dt = start_dt + diff * candlestick_period.value.delta
            else:
                end_dt = start_dt + delta_per_request
            req_parameters["after"] = self._datetime_to_timestamp_ms(end_dt)

            response_json = self._perform_request(ENDPOINT, req_parameters)

            candlesticks_recieved += len(response_json['data'])
            for candlestick_data in response_json['data']:
                yield self._construct_candlestick(candlestick_data)

    def _perform_request(self, url: str, params: dict[str, typing.Any]) -> dict:
        # raises FetchingError, httpx.HTTPError, JSONDecodeError
        response = None
        retries_count = 0
        while response is None:
            try:
                with self._get_http_client() as client:
                    response = client.get(url=url, params=params, timeout=self.TIMEOUT)
                    response.raise_for_status()
            except httpx.HTTPError as e:
                if retries_count == self.RETRY_LIMIT: raise e
                sleep(self.RETRY_TIMEOUT)
            retries_count += 1

        response_json: dict = response.json()

        if response_json["code"] != "0":
            raise FetchingError(
                code=response_json["code"],
                message=response_json["msg"],
            )

        return response_json

    def _datetime_to_timestamp_ms(self, dt: datetime) -> int:
        return int(dt.timestamp() * 1000)

    def _construct_candlestick(self, data: typing.Iterable[typing.Any]) -> Candlestick:
        corresponding_types: tuple[type] = (int, float, float, float, float)
        converted_values = [t(e) for t,e in zip(corresponding_types, data)]

        return Candlestick(*converted_values)

    def get_live_data_client(self) -> ...: ...
