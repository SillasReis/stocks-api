from typing import Optional

from pydantic import BaseModel


class StockCompetitorsMarketCap(BaseModel):
    currency: str
    value: float


class StockCompetitor(BaseModel):
    name: str
    market_cap: StockCompetitorsMarketCap


class StockPerformance(BaseModel):
    five_days: Optional[float] = None
    one_month: Optional[float] = None
    three_months: Optional[float] = None
    ytd: Optional[float] = None
    one_year: Optional[float] = None
