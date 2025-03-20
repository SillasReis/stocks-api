from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session
import structlog

from src.config import Config


logger = structlog.get_logger('database.manager')


class DatabaseSessionManager:
    def __init__(self, host: URL):
        self.engine = create_engine(host)
        self._sessionmaker = sessionmaker(autocommit=False, bind=self.engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        session = self._sessionmaker()
        try:
            logger.debug('DatabaseSessionManager starting session')
            yield session
        except Exception:
            logger.debug('DatabaseSessionManager rollback')
            session.rollback()
            raise
        finally:
            logger.debug('DatabaseSessionManager close session')
            session.close()
