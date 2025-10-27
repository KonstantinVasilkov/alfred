"""Configuration for telegram bot."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict
from shared_infra.config_base import BaseAppSettings


class TelegramBotSettings(BaseAppSettings):
    """Telegram bot specific settings."""

    model_config = SettingsConfigDict(
        env_prefix="TELEGRAM__",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    BOT_TOKEN: str = Field(description="Telegram bot API token")
    ANTHROPIC_API_KEY: str = Field(description="Anthropic API key for LLM interactions")
    LLM_MODEL: str = Field(default="claude-3-haiku-20240307", description="LLM model to use for message processing")


def get_settings() -> TelegramBotSettings:
    """Get telegram bot settings instance."""
    return TelegramBotSettings()  # type: ignore[call-arg]
