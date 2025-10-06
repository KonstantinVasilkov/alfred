"""Configuration for LLM connectors."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from shared_infra.config_base import BaseAppSettings


class LLMConnectorsSettings(BaseAppSettings):
    """LLM connectors specific settings."""

    model_config = SettingsConfigDict(
        env_prefix="LLM_CONNECTORS__",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    API_PORT: int = Field(default=8001, description="API server port")


def get_settings() -> LLMConnectorsSettings:
    """Get LLM connectors settings instance."""
    return LLMConnectorsSettings()  # type: ignore[call-arg]
