class StockDataNotFound(Exception):
    def __init__(self, message: str = "Stock data not found"):
        self.message = message
        super().__init__(self.message)
