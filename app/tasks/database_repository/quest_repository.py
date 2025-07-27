from .base import BaseRepository
import typing
from questdb.ingress import Sender, Protocol
from datetime import timedelta, datetime


class QuestRepository(BaseRepository):
    def __init__(
        self,
        host: str,
        port: int | str,
        username: str | None,
        password: str | None,
        protocol: str = "http",
        *args, **kwargs
    )
        self._protocol = protocol
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._sender: None | Sender = None

    def __enter__(self) -> typing.Self:

        self._sender = Sender(
            protocol=Protocol.parse(self._protocol),
            host=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
        )
        self._sender.__enter__()

        return self

    def __exit__(self) -> None:
        assert self._sender is not None, "__enter__ method must be called before __exit"

        self._sender.__exit__()

    def insert_candlestick(
        self,
        exchange_identifier: str,
        instrument_identifier: str,
        timestamp_dt: datetime,
        period: str,
        open_price: int | float,
        highest_price: int | float,
        lowest_price: int | float,
        close_price: int | float
    ) -> None:
        self._sender.row(
            "market_data",
            symbols={
                "exchange": exchange_identifier.upper(),
                "instrument": instrument_identifier.upper(),
                "period": period.upper(),
            },
            columns={
                "open_price": open_price,
                "highest_price": highest_price,
                "lowest_price": lowest_price,
                "close_price": close_price,
            },
            at=timestamp_dt,
        )
