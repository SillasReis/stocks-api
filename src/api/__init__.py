from fastapi import FastAPI, Response, status
from fastapi.concurrency import asynccontextmanager
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import structlog
import toml

from src.api.routes import stock
from src.api.schema import ErrorResponse
from src.config import Config
from src.core.exception import BaseHttpException
from src.database import __all_models
from src.database.config import start_db


config = Config()
error_logger = structlog.get_logger('api.error')


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_db()
    yield
    

app = FastAPI(
    lifespan=lifespan,
    version=toml.load("pyproject.toml")["project"]["version"],
    title="Stocks API",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=config.LOG_LEVEL == "DEBUG"
)

app.include_router(stock.router)


@app.middleware('http')
async def logging_middleware(request: Request, call_next) -> Response:
    try:
        response = await call_next(request)
    except Exception as e:
        error_logger.error("Uncaught exception", exc_info=True)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        content = ErrorResponse(
            message="Internal Server Error",
        ).model_dump()
        response = JSONResponse(status_code=status_code, content=jsonable_encoder(content))
    finally:
        return response


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    content = ErrorResponse(
        error=exc.errors(),
        message='Validation Error',
    ).model_dump()
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@app.exception_handler(ValueError)
def value_error_exception_handler(request: Request, exc: ValueError):
    status_code = status.HTTP_400_BAD_REQUEST
    content = ErrorResponse(
        message=str(exc),
    ).model_dump()
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@app.exception_handler(BaseHttpException)
def base_exception_handler(request: Request, exc: BaseHttpException):
    status_code = exc.status_code
    content = ErrorResponse(
        error=exc.errors(),
        message=exc.message,
    ).model_dump()
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
