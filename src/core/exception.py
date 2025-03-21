from fastapi import HTTPException


class BaseHttpException(HTTPException):
    def __init__(self, status_code, message):
        super().__init__(status_code, message)
        self.message = message

    def errors(self):
        return []
