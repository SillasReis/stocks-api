from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    error: dict | list[dict] = None
