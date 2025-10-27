"""Configuration for finances API."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict
from shared_infra.config_base import BaseAppSettings


class FinancesSettings(BaseAppSettings):
    """Finances API specific settings."""

    model_config = SettingsConfigDict(
        env_prefix="FINANCES__",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    DB_DSN: str = Field(description="Database connection string")
    API_PORT: int = Field(default=8000, description="API server port")


def get_settings() -> FinancesSettings:
    """Get finances API settings instance."""
    return FinancesSettings()  # type: ignore[call-arg]
