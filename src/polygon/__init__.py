from datetime import date

from src.config import Config
from src.polygon.exceptions import StockDataNotFound
from src.polygon.shcema import StockDailyInfo
from src.requester import Requester, HTTPError


class Polygon:
    def __init__(self):
        self.config = Config()

    def get_stock_daily_info(self, stock_symbol: str, date: date) -> StockDailyInfo:
        url = f"{self.config.POLYGON_BASE_URL}/v1/open-close/{stock_symbol}/{date.strftime('%Y-%m-%d')}"

        try:
            response = Requester(
                "GET",
                url=url,
                headers={"Authorization": f"Bearer {self.config.POLYGON_API_KEY}"}
            ).response
        except HTTPError as e:
            if e.response.status_code == 404 and e.response.json().get("message").lower() == "data not found.":
                raise StockDataNotFound
            else:
                raise e

        return StockDailyInfo.model_validate(response.json())
