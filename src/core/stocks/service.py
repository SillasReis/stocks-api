from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.config import Config
from src.core.stocks.exception import StockNotFound
from src.core.stocks.repository import StockRepository
from src.core.stocks.schema import StockResponse
from src.polygon import Polygon
from src.polygon.exceptions import StockDataNotFound
from src.polygon.shcema import StockDailyInfo
from src.scraper.marketwatch_stock import MarketWatchStockScraper


config = Config()


class StockService:
    def __init__(self, session: Session):
        self.repository = StockRepository(session)

    @staticmethod
    def __get_last_valid_stock_daily_info(stock_symbol: str) -> tuple[date, StockDailyInfo]:
        success_flag = False
        from_date = date.today() - timedelta(days=1)
        attempts = 0

        while not success_flag:
            try:
                stock_daily_info = Polygon.get_stock_daily_info(stock_symbol, from_date)
                success_flag = True
            except StockDataNotFound:
                from_date -= timedelta(days=1)
                attempts += 1

                if attempts >= config.STOCK_DAILY_INFO_MAX_ATTEMPTS:
                    raise StockNotFound
    
        return from_date,stock_daily_info

    def get(self, symbol: str) -> StockResponse:
        symbol = symbol.upper()

        from_date, stock_daily_info = StockService.__get_last_valid_stock_daily_info(symbol)

        market_watch_scraper = MarketWatchStockScraper(symbol)
        competitors = market_watch_scraper.get_stock_competitors()
        performance = market_watch_scraper.get_stock_performance()
        company_name = market_watch_scraper.get_stock_company_name()

        stock_record = self.repository.get_by_symbol(symbol)

        response = StockResponse.model_validate({
            "status": stock_daily_info.status,
            "purchased_amount": stock_record.purchased_amount if stock_record else 0,
            # "purchased_status": "???",
            "request_data": from_date,
            "company_code": symbol,
            "company_name": company_name,
            "stock_values": stock_daily_info,
            "performance_data": performance,
            "competitors": competitors
        }, from_attributes=True)

        return response
