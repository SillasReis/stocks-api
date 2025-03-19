from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    REQUESTER_RETRY_MAX: int = 5
    REQUESTER_TIMEOUT: int = 20
    REQUESTER_ALLOW_REDIRECTS: bool = True
    REQUESTER_STREAM: bool = True
    REQUESTER_VERIFY: bool = False

    POLYGON_BASE_URL: str
    POLYGON_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=('.env'),
        extra='ignore',
    )
