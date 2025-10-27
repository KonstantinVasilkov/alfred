"""Base configuration class with common settings for all apps."""

from pydantic import Field
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base settings class with common configuration fields."""

    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment (development/staging/production)")

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE_ENABLED: bool = Field(default=True, description="Enable file logging")
    LOG_FILE_PATH: str = Field(default="./logs", description="Directory path for log files")
    LOG_FILE_RETENTION_DAYS: int = Field(default=7, description="Number of days to retain log files")
    LOG_FILE_ROTATION: str = Field(default="1 day", description="Log file rotation interval")

    # OpenTelemetry Configuration
    OTEL_ENABLED: bool = Field(default=False, description="Enable OpenTelemetry instrumentation")
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(default="https://api.honeycomb.io", description="OTLP endpoint URL")
    OTEL_SERVICE_NAME: str = Field(default="app", description="Service name for telemetry")
    HONEYCOMB_API_KEY: str | None = Field(default=None, description="Honeycomb API key for OTLP export")

    # Error Tracking
    SENTRY_DSN: str | None = Field(default=None, description="Sentry DSN for error tracking")
