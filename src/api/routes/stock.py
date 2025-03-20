from fastapi import APIRouter, Path

from src.core.stocks.schema import StockResponse
from src.core.stocks.service import StockService
from src.database import SessionDep


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
