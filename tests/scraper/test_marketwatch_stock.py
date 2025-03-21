from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from src.scraper.marketwatch_stock import MarketWatchStockScraper


@pytest.fixture
def mock_stock_page_content():
    return """
    <html>
        <body>
            <h1 class="company__name">Apple Inc.</h1>
            <div class="element element--table competitor-data">
                <table aria-label="Competitors data table">
                    <tbody>
                        <tr>
                            <td><a href="/investing/stock/MSFT">Microsoft Corp.</a></td>
                            <td class="table__cell w25 number">$350.5B</td>
                        </tr>
                        <tr>
                            <td><a href="/investing/stock/GOOGL">Alphabet Inc.</a></td>
                            <td class="table__cell w25 number">$280.2B</td>
                        </tr>
                        <tr>
                            <td><a href="/investing/stock/992">Lenovo Group Ltd.</a></td>
                            <td class="table__cell w25 number">HK$144.89T</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="element element--table performance">
                <table class="table table--primary no-heading c2">
                    <tbody>
                        <tr>
                            <td>5 Day</td>
                            <td><li class="content__item value ignore-color">2.5%</li></td>
                        </tr>
                        <tr>
                            <td>1 Month</td>
                            <td><li class="content__item value ignore-color">5.8%</li></td>
                        </tr>
                        <tr>
                            <td>3 Month</td>
                            <td><li class="content__item value ignore-color">10.2%</li></td>
                        </tr>
                        <tr>
                            <td>YTD</td>
                            <td><li class="content__item value ignore-color">15.3%</li></td>
                        </tr>
                        <tr>
                            <td>1 Year</td>
                            <td><li class="content__item value ignore-color">22.1%</li></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """

@pytest.fixture
def mock_scraper(mock_stock_page_content):
    with patch('src.scraper.marketwatch_stock.Requester') as mock_requester:
        mock_response = Mock()
        mock_response.text = mock_stock_page_content
        mock_requester.return_value.response = mock_response
        
        scraper = MarketWatchStockScraper("AAPL")
        yield scraper

class TestMarketWatchStockScraper:
    def test_get_stock_company_name(self, mock_scraper):
        company_name = mock_scraper.get_stock_company_name()
        assert company_name == "Apple Inc."

    def test_get_stock_competitors(self, mock_scraper):
        competitors = mock_scraper.get_stock_competitors()
        assert len(competitors) == 3
        assert competitors[0].name == "Microsoft Corp."
        assert competitors[0].market_cap.currency == "$"
        assert competitors[0].market_cap.value == 350.5e9
        assert competitors[1].name == "Alphabet Inc."
        assert competitors[1].market_cap.currency == "$"
        assert competitors[1].market_cap.value == 280.2e9
        assert competitors[2].name == "Lenovo Group Ltd."
        assert competitors[2].market_cap.currency == "HK$"
        assert competitors[2].market_cap.value == 144.89e12

    def test_get_stock_performance(self, mock_scraper):
        performance = mock_scraper.get_stock_performance()
        assert performance.five_days == 2.5
        assert performance.one_month == 5.8
        assert performance.three_months == 10.2
        assert performance.ytd == 15.3
        assert performance.one_year == 22.1

    @pytest.mark.parametrize("value,expected", [
        ("1.5T", Decimal("1.5e12")),
        ("500B", Decimal("5e11")),
        ("100M", Decimal("1e8")),
        ("50K", Decimal("5e4")),
        ("1234", Decimal("1234")),
        ("1.5", Decimal("1.5")),
    ])
    def test_convert_market_value(self, value, expected):
        result = MarketWatchStockScraper._MarketWatchStockScraper__convert_market_value(value)
        assert result == float(expected)

    def test_scraper_with_empty_response(self):
        with patch('src.scraper.marketwatch_stock.Requester') as mock_requester:
            mock_response = Mock()
            mock_response.text = "<html><body></body></html>"
            mock_requester.return_value.response = mock_response
            
            scraper = MarketWatchStockScraper("AAPL")
            
            with pytest.raises(Exception):
                scraper.get_stock_company_name()

            with pytest.raises(Exception):
                scraper.get_stock_performance()

            assert scraper.get_stock_competitors() == []
