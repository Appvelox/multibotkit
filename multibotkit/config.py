from pydantic import BaseSettings


class Settings(BaseSettings):

    SENTRY_ENVIRONMENT: str
    SENTRY_SERVER: str
    SENTRY_DSN: str


settings = Settings()