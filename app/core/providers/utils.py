from .common import CandlestickPeriod


def get_candlestick_period_from_string(data: str) -> CandlestickPeriod | None:
    for period in CandlestickPeriod:
        if period.value.id.lower() == data.lower():
            return period
