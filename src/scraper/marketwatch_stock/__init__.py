from decimal import Decimal
import re

from bs4 import BeautifulSoup
import structlog

from src.requester import Requester
from src.scraper.marketwatch_stock.schema import StockPerformance, StockCompetitor


logger = structlog.get_logger("scraper.marketwatch_stock")


class MarketWatchStockScraper:
    BASE_URL = "https://www.marketwatch.com"
    HEADERS = {
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    STOCK_PERFORMANCE_MAPPING = {
        "5 Day": "five_days",
        "1 Month": "one_month",
        "3 Month": "three_months",
        "YTD": "ytd",
        "1 Year": "one_year",
    }

    def __init__(self, stock_symbol: str):
        self.stock_url = f"{MarketWatchStockScraper.BASE_URL}/investing/stock/{stock_symbol}"
        self.stock_page_content: BeautifulSoup = self.__get_stock_page_content()

    def __get_stock_page_content(self) -> BeautifulSoup:
        response = Requester("GET", self.stock_url, headers=MarketWatchStockScraper.HEADERS).response
        return BeautifulSoup(response.text, 'html.parser')

    @staticmethod
    def __convert_market_value(value: str) -> float:
        multipliers = {
            'T': Decimal(1e12),
            'B': Decimal(1e9),
            'M': Decimal(1e6),
            'K': Decimal(1e3)
        }

        value = value.strip()
        suffix = value[-1].upper()

        if suffix not in multipliers:
            return float(value)

        number = Decimal(value[:-1])
        return float(number * multipliers[suffix])

    def get_stock_performance(self) -> StockPerformance:
        response = {}
        
        try:
            rows = self.stock_page_content.find("table", "table table--primary no-heading c2").find("tbody").find_all("tr")
        except AttributeError:
            raise Exception("Stock performance table not found")

        for row in rows:
            period = row.find("td")
            performance = row.find("li", "content__item value ignore-color")

            if not period or not performance:
                continue

            mapped_period = MarketWatchStockScraper.STOCK_PERFORMANCE_MAPPING.get(period.text)
            
            if not mapped_period:
                continue

            response[mapped_period] = float(performance.text[0:-1])
        
        return StockPerformance.model_validate(response)

    def get_stock_competitors(self) -> list[StockCompetitor]:
        response = []
        
        try:
            competitors = self.stock_page_content.find("table", {"aria-label": "Competitors data table"}).find("tbody").find_all("tr")
        except AttributeError:
            competitors = []
            logger.info("Stock competitors table not found")

        for competitor in competitors:
            name = competitor.find("a")
            market_cap = competitor.find("td", {"class": "table__cell w25 number"})

            if not name or not market_cap:
                continue

            currency = re.match(r'^[^0-9]+', market_cap.text).group()
            value = market_cap.text.replace(currency, "")

            response.append({
                "name": name.text,
                "market_cap": {
                    "currency": currency,
                    "value": MarketWatchStockScraper.__convert_market_value(value)
                }
            })
        
        return [StockCompetitor.model_validate(r) for r in response]

    def get_stock_company_name(self) -> str:
        company_name = self.stock_page_content.find("h1", {"class": "company__name"})
        
        if not company_name:
            raise Exception("Stock company name not found")

        return company_name.text
