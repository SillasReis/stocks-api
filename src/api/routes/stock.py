from decimal import Decimal

from fastapi import APIRouter, Path

from src.core.stocks.schema import StockPurchaseRequest,StockResponse
from src.core.stocks.service import StockService
from src.database import SessionDep
from src.api.schema import MessageResponse


router = APIRouter(prefix="/stock")


@router.get(
    "/{stock_symbol}",
    status_code=200,
    response_model=StockResponse
)
def get_stock(
    db_session: SessionDep,
    stock_symbol: str = Path(..., description="Stock symbol", example="AAPL", max_length=20)
):
    service = StockService(db_session)
    return service.get(stock_symbol)


@router.post(
    "/{stock_symbol}",
    status_code=201,
    response_model=MessageResponse
)
def purchase_stock(
    db_session: SessionDep,
    stock_purchase_request: StockPurchaseRequest,
    stock_symbol: str = Path(..., description="Stock symbol", example="AAPL", max_length=20)
):
    service = StockService(db_session)
    service.purchase(stock_symbol, stock_purchase_request.amount)
    return MessageResponse(message=f"{stock_purchase_request.amount} units of stock {stock_symbol} were added to your stock record")
