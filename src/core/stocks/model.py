from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model import Base


class Stock(Base):
    __tablename__ = "stocks"

    symbol: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    purchased_amount: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"Stock(symbol={self.symbol}, purchased_amount={self.purchased_amount})"
