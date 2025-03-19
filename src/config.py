from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    RETRY_MAX: int = 5
    TIMEOUT: int = 20
    ALLOW_REDIRECTS: bool = True
    STREAM: bool = True
    VERIFY: bool = False

    model_config = SettingsConfigDict(
        env_file=('.env'),
        extra='ignore',
    )
