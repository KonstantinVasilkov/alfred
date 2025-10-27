import asyncio

from llm.factory import create_agent
from shared_infra import get_logger, setup_observability

from telegram_bot.bot import run_bot
from telegram_bot.config import get_settings
from telegram_bot.message_service import MessageService


def main() -> None:
    """Entry point for the application."""
    settings = get_settings()

    # Setup observability (logging, OTEL, Sentry)
    setup_observability(settings)
    logger = get_logger(__name__)

    try:
        logger.info(
            "telegram_bot_starting",
            environment=settings.ENVIRONMENT,
            log_level=settings.LOG_LEVEL,
            otel_enabled=settings.OTEL_ENABLED,
        )

        # Create LLM agent and message service
        llm_agent = create_agent(api_key=settings.ANTHROPIC_API_KEY, model=settings.LLM_MODEL)
        message_service = MessageService(llm_agent=llm_agent)

        logger.info("telegram_bot_initialized", llm_model=settings.LLM_MODEL)

        # Run the bot
        asyncio.run(run_bot(token=settings.BOT_TOKEN, message_service=message_service))

    except Exception as e:
        logger.exception(
            "telegram_bot_startup_failed",
            error_type=type(e).__name__,
            extra={"sentry_fingerprint": ["telegram-bot-startup-failed"]},
        )
        raise


if __name__ == "__main__":
    main()
