from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from requests import Response

from src.polygon import Polygon
from src.polygon.exceptions import StockDataNotFound
from src.requester import HTTPError


@pytest.fixture
def mock_success_response():
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

class TestPolygon:
    def test_get_stock_daily_info_success(self, mock_success_response):
        with patch('src.polygon.Requester') as mock_requester:
            # Setup mock response
            mock_response = Mock(spec=Response)
            mock_response.json.return_value = mock_success_response
            mock_requester.return_value.response = mock_response

            # Test the API call
            test_date = date(2025, 3, 19)
            result = Polygon.get_stock_daily_info("AAPL", test_date)

            # Verify the result
            assert result.status == "OK"
            assert result.open == 100.00
            assert result.high == 105.00
            assert result.low == 98.00
            assert result.close == 102.00
            assert result.volume == 1000000
            assert result.after_hours == 102.50
            assert result.pre_market == 99.50

    def test_get_stock_daily_info_not_found(self):
        with patch('src.polygon.Requester') as mock_requester:
            # Setup mock error response
            mock_response = Mock(spec=Response)
            mock_response.status_code = 404
            mock_response.json.return_value = {
                "message": "Data not found."
            }
            
            # Setup the HTTP error
            http_error = HTTPError(response=mock_response)
            mock_requester.side_effect = http_error

            # Test the API call
            test_date = date(2025, 3, 19)
            with pytest.raises(StockDataNotFound):
                Polygon.get_stock_daily_info("INVALID", test_date)

    def test_get_stock_daily_info_other_error(self):
        with patch('src.polygon.Requester') as mock_requester:
            # Setup mock error response for a different error
            mock_response = Mock(spec=Response)
            mock_response.status_code = 500
            mock_response.json.return_value = {
                "message": "Internal server error"
            }
            
            # Setup the HTTP error
            http_error = HTTPError(response=mock_response)
            mock_requester.side_effect = http_error

            # Test the API call
            test_date = date(2025, 3, 19)
            with pytest.raises(HTTPError):
                Polygon.get_stock_daily_info("AAPL", test_date)
