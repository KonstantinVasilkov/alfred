"""Base configuration class with common settings for all apps."""

from pydantic import Field
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base settings class with common configuration fields."""

    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    SENTRY_DSN: str | None = Field(default=None, description="Sentry DSN for error tracking")
