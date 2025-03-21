from decimal import Decimal

import pytest
from sqlalchemy.exc import NoResultFound

from src.core.stocks.model import Stock
from src.core.stocks.repository import StockRepository


@pytest.fixture
def stock_repository(db_session):
    return StockRepository(db_session)

@pytest.fixture
def sample_stock():
    return Stock(symbol="AAPL", purchased_amount=Decimal("100.00"))

class TestStockRepository:
    def test_add_stock(self, stock_repository, sample_stock):
        added_stock = stock_repository.add(sample_stock)

        assert added_stock.symbol == "AAPL"
        assert added_stock.purchased_amount == Decimal("100.00")

        # Verify persistence
        found_stock = stock_repository.get_by_symbol("AAPL")
        assert found_stock.symbol == "AAPL"
        assert found_stock.purchased_amount == Decimal("100.00")

    def test_get_by_symbol_existing(self, stock_repository, sample_stock):
        stock_repository.add(sample_stock)
        found_stock = stock_repository.get_by_symbol("AAPL")
        assert found_stock.symbol == "AAPL"
        assert found_stock.purchased_amount == Decimal("100.00")

    def test_get_by_symbol_non_existing(self, stock_repository):
        found_stock = stock_repository.get_by_symbol("NONEXISTENT")
        assert found_stock is None

    def test_update_by_symbol_existing(self, stock_repository, sample_stock):
        stock_repository.add(sample_stock)
        updated_stock = stock_repository.update_by_symbol(
            "AAPL", 
            {"purchased_amount": Decimal("150.00")}
        )
        assert updated_stock.purchased_amount == Decimal("150.00")
        
        # Verify persistence
        found_stock = stock_repository.get_by_symbol("AAPL")
        assert found_stock.purchased_amount == Decimal("150.00")

    def test_update_by_symbol_non_existing(self, stock_repository):
        with pytest.raises(NoResultFound):
            stock_repository.update_by_symbol(
                "NONEXISTENT", 
                {"purchased_amount": Decimal("150.00")}
            )

    def test_multiple_stocks(self, stock_repository):
        stocks = [
            Stock(symbol="AAPL", purchased_amount=Decimal("100.00")),
            Stock(symbol="GOOGL", purchased_amount=Decimal("200.00")),
            Stock(symbol="MSFT", purchased_amount=Decimal("150.00"))
        ]
        
        for stock in stocks:
            stock_repository.add(stock)
        
        for stock in stocks:
            found = stock_repository.get_by_symbol(stock.symbol)
            assert found.symbol == stock.symbol
            assert found.purchased_amount == stock.purchased_amount
