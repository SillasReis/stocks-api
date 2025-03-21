from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from src.core.stocks.model import Stock


@pytest.fixture
def sample_stock():
    return Stock(
        symbol="AAPL",
        purchased_amount=Decimal("100.00")
    )


@pytest.fixture
def mock_redis():
    with patch("redis.Redis") as mock_redis:
        mock_client = Mock()
        mock_redis.from_url.return_value = mock_client
        yield mock_client
