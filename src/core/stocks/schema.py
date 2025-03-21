from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )


class StockValuesResponse(BaseSchema):
    open: float
    high: float
    low: float
    close: float


class StockPerformanceResponse(BaseSchema):
    five_days: Optional[float] = None
    one_month: Optional[float] = None
    three_months: Optional[float] = None
    ytd: Optional[float] = Field(None, alias="year_to_date")
    one_year: Optional[float] = None


class StockCompetitorsMarketCapResponse(BaseSchema):
    currency: str = Field(..., alias="Currency")
    value: float = Field(..., alias="Value")


class StockCompetitorResponse(BaseSchema):
    name: str
    market_cap: StockCompetitorsMarketCapResponse


class StockPurchaseRequest(BaseSchema):
    amount: Decimal = Field(..., description="Amount to purchase", decimal_places=2)


class StockResponse(BaseSchema):
    status: str = Field(..., alias="Status")
    purchased_amount: float
    # purchased_status: str
    request_data: date
    company_code: str
    company_name: str
    stock_values: StockValuesResponse = Field(..., alias="Stock_values")
    performance_data: StockPerformanceResponse
    competitors: list[StockCompetitorResponse] = Field(..., alias="Competitors")

    @field_serializer("request_data")
    def serialize_date(self, date: date) -> str:
        return date.strftime('%Y-%m-%d')
