from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

import toml

from src.config import Config
from src.database import __all_models
from src.database.config import start_db

config = Config()

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
