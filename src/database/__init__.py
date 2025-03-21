from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from src.database.config import get_db_session


SessionDep = Annotated[Session, Depends(get_db_session)]
