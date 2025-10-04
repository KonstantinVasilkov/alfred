from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    telegram_bot_token: str = Field(description="Telegram bot API token")
    anthropic_api_key: str = Field(description="Anthropic API key for LLM interactions")
    llm_model: str = Field(
        default="claude-3-haiku-20240307", description="LLM model to use for message processing"
    )


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()  # type: ignore[call-arg]
