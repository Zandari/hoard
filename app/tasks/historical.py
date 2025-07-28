from app.celery import celery_app
from .data_providers import OKXMarketProvider
from .data_providers.utils import get_candlestick_period_from_string
from .database_repository.factory import RepositoryFactory
from datetime import datetime
from app.config import Config


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

    database_repository = RepositoryFactory.make_repository_from_url(
        url=Config.DATABASE_URL,
        table_name=Config.MARKET_DATA_TABLE_NAME,
    )
    with database_repository as db_repo:
        for candlestick in candlestick_generator:
            db_repo.insert_candlestick(
                exchange_identifier=exchange_identifier,
                instrument_identifier=instrument_identifier,
                timestamp_dt=datetime.utcfromtimestamp(
                    candlestick.timestamp_ms / 1000.0
                ),
                period=candlestick_period.value.id,
                open_price=candlestick.open_price,
                highest_price=candlestick.highest_price,
                lowest_price=candlestick.lowest_price,
                close_price=candlestick.close_price,
            )

            progress_state_meta["completed"] += 1
            self.update_state(state="PROGRESS", meta=progress_state_meta)
