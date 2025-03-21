from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from src.core.stocks.exception import InvalidPurchaseAmount, StockNotFound
from src.core.stocks.model import Stock
from src.core.stocks.schema import StockPerformanceResponse, StockCompetitorResponse, StockCompetitorsMarketCapResponse
from src.core.stocks.service import StockService
from src.polygon.exceptions import StockDataNotFound
from src.polygon.shcema import StockDailyInfo


@pytest.fixture
def stock_service(db_session: Session, mock_redis):
    service = StockService(db_session)
    service.cacher.client = mock_redis
    return service


@pytest.fixture
def mock_stock_daily_info():
    return {
        "status": "OK",
        "from": "2025-03-19",
        "symbol": "AAPL",
        "open": 100.00,
        "high": 105.00,
        "low": 98.00,
        "close": 102.00,
        "volume": 1000000,
        "afterHours": 102.50,
        "preMarket": 99.50
    }


@pytest.fixture
def mock_stock_competitors():
    return [
        StockCompetitorResponse(
            name="Microsoft Corp.",
            market_cap=StockCompetitorsMarketCapResponse(
                Currency="$",
                Value=350.5e9
            )
        ),
        StockCompetitorResponse(
            name="Alphabet Inc.",
            market_cap=StockCompetitorsMarketCapResponse(
                Currency="$",
                Value=280.2e9
            )
        )
    ]


@pytest.fixture
def mock_stock_performance():
    return StockPerformanceResponse(
        five_days=2.5,
        one_month=5.8,
        three_months=10.2,
        year_to_date=15.3,
        one_year=25.7
    )


class TestStockService:
    def test_get_stock_success(self, stock_service, mock_stock_daily_info, mock_stock_competitors, mock_stock_performance):
        symbol = "AAPL"
        with patch("src.core.stocks.service.Polygon") as mock_polygon, \
             patch("src.core.stocks.service.MarketWatchStockScraper") as mock_scraper:
            
            stock_service.cacher.client.get.return_value = None
            
            mock_polygon.get_stock_daily_info.return_value = StockDailyInfo.model_validate(mock_stock_daily_info)
            
            mock_scraper_instance = Mock()
            mock_scraper_instance.get_stock_competitors.return_value = mock_stock_competitors
            mock_scraper_instance.get_stock_performance.return_value = mock_stock_performance
            mock_scraper_instance.get_stock_company_name.return_value = "Apple Inc."
            mock_scraper.return_value = mock_scraper_instance

            response = stock_service.get(symbol)
            
            assert response.status == "OK"
            assert response.company_code == symbol
            assert response.company_name == "Apple Inc."
            assert response.purchased_amount == 0
            assert response.stock_values.open == 100.00
            assert response.stock_values.high == 105.00
            assert response.stock_values.low == 98.00
            assert response.stock_values.close == 102.00
            assert response.competitors == mock_stock_competitors
            assert response.performance_data == mock_stock_performance

    def test_get_stock_from_cache(self, stock_service):
        symbol = "AAPL"
        cached_data = '{"Status":"OK","purchased_amount":0,"request_data":"2025-03-19","company_code":"AAPL","company_name":"Apple Inc.","stock_values":{"status":"OK","from":"2025-03-19","symbol":"AAPL","open":100.0,"high":105.0,"low":98.0,"close":102.0,"volume":1000000,"afterHours":102.5,"preMarket":99.5},"performance_data":{"five_days":2.5,"one_month":5.8,"three_months":10.2,"year_to_date":15.3,"one_year":25.7},"competitors":[{"name":"Microsoft Corp.","market_cap":{"Currency":"$","Value":350500000000.0}},{"name":"Alphabet Inc.","market_cap":{"Currency":"$","Value":280200000000.0}}]}'
        
        stock_service.cacher.client.get.return_value = cached_data.encode()
        response = stock_service.get(symbol)
        
        assert response.status == "OK"
        assert response.company_code == symbol
        assert response.company_name == "Apple Inc."
        assert response.purchased_amount == 0
        assert response.stock_values.open == 100.00
        assert response.stock_values.high == 105.00
        assert response.stock_values.low == 98.00
        assert response.stock_values.close == 102.00

    def test_get_stock_not_found(self, stock_service):
        symbol = "INVALID"
        with patch("src.core.stocks.service.Polygon") as mock_polygon:
            stock_service.cacher.client.get.return_value = None
            mock_polygon.get_stock_daily_info.side_effect = StockDataNotFound
            
            with pytest.raises(StockNotFound):
                stock_service.get(symbol)

    def test_purchase_stock_new(self, stock_service, mock_stock_daily_info):
        symbol = "AAPL"
        amount = Decimal("100.00")
        
        with patch("src.core.stocks.service.Polygon") as mock_polygon:
            mock_polygon.get_stock_daily_info.return_value = StockDailyInfo.model_validate(mock_stock_daily_info)
            
            stock_service.purchase(symbol, amount)
            
            stock = stock_service.repository.get_by_symbol(symbol)
            assert stock.symbol == symbol
            assert stock.purchased_amount == amount
            stock_service.cacher.client.delete.assert_called_once_with("stocks:AAPL")

    def test_purchase_stock_update(self, stock_service):
        symbol = "AAPL"
        initial_amount = Decimal("100.00")
        additional_amount = Decimal("50.00")
        
        stock_service.repository.add(Stock(symbol=symbol, purchased_amount=initial_amount))
        
        stock_service.purchase(symbol, additional_amount)
        
        stock = stock_service.repository.get_by_symbol(symbol)
        assert stock.symbol == symbol
        assert stock.purchased_amount == initial_amount + additional_amount
        stock_service.cacher.client.delete.assert_called_once_with("stocks:AAPL")

    def test_purchase_stock_invalid_amount(self, stock_service):
        symbol = "AAPL"
        initial_amount = Decimal("100.00")
        invalid_amount = Decimal("-150.00")
        
        stock_service.repository.add(Stock(symbol=symbol, purchased_amount=initial_amount))
        
        with pytest.raises(InvalidPurchaseAmount):
            stock_service.purchase(symbol, invalid_amount)
