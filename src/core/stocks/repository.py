from src.core.stocks.model import Stock
from src.database.repository import BaseRepository


class StockRepository(BaseRepository[Stock]):
    def get_by_symbol(self, symbol: str) -> Stock:
        return self.get_one_by_column(Stock, column="symbol", value=symbol)

    def update_by_symbol(self, symbol: str, data: dict) -> Stock:
        return self.update_one(Stock, column="symbol", value=symbol, data=data)
