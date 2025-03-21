from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


class BaseRepository[T]:
    def __init__(self, session: Session):
        self.session = session
    
    def commit(self):
        self.session.commit()

    def execute(self, query):
        result = self.session.execute(query)
        return result

    def flush(self):
        self.session.flush()
    
    def rollback(self):
        self.session.rollback()

    def refresh(self, model: T):
        self.session.refresh(model)

    def add(self, model: T) -> T:
        self.session.add(model)
        self.commit()
        self.refresh(model)
        return model

    def get_one_by_column(self, model: T, *, value: str | int, column: str = "id") -> T:
        query = select(model).where(getattr(model, column) == value)
        results = self.execute(query)
        return results.unique().scalar_one_or_none()
    
    def update_one(self, model: T, *, value: str | int, data: dict, column: str = "id") -> T:
        db_model = self.get_one_by_column(model, value=value, column=column)

        if not db_model:
            raise NoResultFound

        for k, v in data.items():
            setattr(db_model, k, v)

        self.commit()
        self.refresh(db_model)

        return db_model
