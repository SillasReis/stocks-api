from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(MessageResponse):
    error: dict | list[dict] = None
