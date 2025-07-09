from app.celery import celery_app
from .data_providers import OKXMarketProvider
from .data_providers.utils import get_candlestick_period_from_string
from datetime import datetime
from app.config import Config
from questdb.ingress import Sender, TimestampNanos


@celery_app.task(bind=True)
def fetch_historical_data_task(
    self,
    exchange_identifier: str,
    instrument_identifier: str,
    start_dt: datetime,
    end_dt: datetime,
    period: str
) -> bool:
    provider = OKXMarketProvider()

    candlestick_period = get_candlestick_period_from_string(period)

    if candlestick_period is None:
        raise ValueError(f"Unknows candlestick period provided: {period}")

    candlestick_generator = provider.fetch_historical_market_data(
        instrument=instrument_identifier,
        start=start_dt,
        end=end_dt,
        candlestick_period=candlestick_period
    )

    estimated_candles_amount = provider.get_estimated_candlestick_amount(
        start=start_dt,
        end=end_dt,
        candlestick_period=candlestick_period,
    )
    progress_state_meta = {
        "total": estimated_candles_amount,
        "completed": 0,
    }

    self.update_state(state="PROGRESS", meta=progress_state_meta)

    with Sender.from_conf(Config.QUESTDB_CONF) as sender:
        for candlestick in candlestick_generator:
            sender.row(
                "market_data",
                symbols={
                    "exchange": exchange_identifier.upper(),
                    "instrument": instrument_identifier.upper(),
                    "period": candlestick_period.value.id.upper(),
                },
                columns={
                    "open_price": candlestick.open_price,
                    "highest_price": candlestick.highest_price,
                    "lowest_price": candlestick.lowest_price,
                    "close_price": candlestick.close_price,
                },
                at=TimestampNanos(candlestick.timestamp_ms * 1000 * 1000),
            )
            progress_state_meta["completed"] += 1
            self.update_state(state="PROGRESS", meta=progress_state_meta)
