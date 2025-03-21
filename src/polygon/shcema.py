from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class StockDailyInfo(BaseModel):
    status: str
    from_date: date = Field(alias="from")
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    after_hours: Optional[float] = Field(None, alias="afterHours")
    pre_market: Optional[float] = Field(None, alias="preMarket")
