from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    REQUESTER_RETRY_MAX: int = 5
    REQUESTER_TIMEOUT: int = 20
    REQUESTER_ALLOW_REDIRECTS: bool = True
    REQUESTER_STREAM: bool = True
    REQUESTER_VERIFY: bool = False

    POLYGON_BASE_URL: str
    POLYGON_API_KEY: str

    DB_PROTOCOL: str = "postgresql+psycopg"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_URL: str
    CACHE_TTL_SECONDS: int = 3600

    LOG_LEVEL: str = "INFO"

    STOCK_DAILY_INFO_MAX_ATTEMPTS: int = 5

    model_config = SettingsConfigDict(
        env_file=('.env'),
        extra='ignore',
    )
