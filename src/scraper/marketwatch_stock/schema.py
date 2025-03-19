from pydantic import BaseModel


class StockCompetitorsMarketCap(BaseModel):
    currency: str
    value: float


class StockCompetitor(BaseModel):
    name: str
    market_cap: StockCompetitorsMarketCap


class StockPerformance(BaseModel):
    five_days: float
    one_month: float
    three_months: float
    ytd: float
    one_year: float
