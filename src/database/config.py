from contextlib import contextmanager
from typing import Iterator

from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from src.config import Config
from src.database.manager import DatabaseSessionManager
from src.database.model import Base


config = Config()
url = URL.create(
    config.DB_PROTOCOL,
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME
)


def get_db_session() -> Iterator[Session]:
    session_manager = DatabaseSessionManager(url)
    with session_manager.session() as session:
        yield session


@contextmanager
def context_get_db_session():
    session_manager = DatabaseSessionManager(url)
    with session_manager.session() as session:
        yield session


def start_db():
    session_manager = DatabaseSessionManager(url)
    Base.metadata.create_all(session_manager.engine, checkfirst=True)
