from src.core.exception import BaseHttpException


class StockNotFound(BaseHttpException):
    def __init__(self, message: str = "Stock not found"):
        super().__init__(404, message)


class InvalidPurchaseAmount(BaseHttpException):
    def __init__(self, message: str = "Invalid purchase amount. Total value can't be negative."):
        super().__init__(400, message)
