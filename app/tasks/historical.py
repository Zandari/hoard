from app.celery import celery_app
from app.core.providers import (
    OKXMarketProvider,
    CandlestickPeriod,
    Candlestick
)
from app.core.providers.utils import get_candlestick_period_from_string
from datetime import datetime, timedelta
from app.config import Config
from questdb.ingress import Sender, TimestampMicros
import typing
import asyncio


async def asdf(
    exchange_identifier: str,
    instrument_identifier: str,
    start_dt: datetime,
    end_dt: datetime,
    period: str
):
    provider = OKXMarketProvider()

    candlestick_period = get_candlestick_period_from_string(period)

    if candlestick_period is None:
        raise ValueError(f"Unknows candlestick period provided: {period}")

    candlestick_iterator = provider.fetch_historical_market_data(
        instrument=exchange_identifier,
        start=start_dt,
        end=end_dt,
        candlestick_period=candlestick_period
    )

    table_name = "{}-{}-{}".format(
        exchange_identifier.upper(),
        instrument_identifier.upper(),
        candlestick_period.value.id.upper()
    )

    with Sender.from_conf(Config.QUESTDB_CONF) as sender:
        async for candlestick in candlestick_iterator:
            sender.row(
                table_name,
                columns={
                    "open_price": candlestick.open_price,
                    "highest_price": candlestick.highest_price,
                    "lowest_price": candlestick.lowest_price,
                    "close_price": candlestick.close_price,
                },
                at=TimestampMicros(candlestick.timestamp_ms),
            )

@celery_app.task()
def fetch_historical_data(
    exchange_identifier: str,
    instrument_identifier: str,
    start_dt: datetime,
    end_dt: datetime,
    period: str
) -> bool:
    asyncio.run(asdf(
        exchange_identifier,
        instrument_identifier,
        start_dt,
        end_dt,
        period,
    ))
