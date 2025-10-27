import asyncio

from llm.factory import create_agent

from telegram_bot.bot import run_bot
from telegram_bot.config import get_settings
from telegram_bot.message_service import MessageService


def main() -> None:
    """Entry point for the application."""
    settings = get_settings()

    # Create LLM agent and message service
    llm_agent = create_agent(api_key=settings.ANTHROPIC_API_KEY, model=settings.LLM_MODEL)
    message_service = MessageService(llm_agent=llm_agent)

    # Run the bot
    asyncio.run(run_bot(token=settings.BOT_TOKEN, message_service=message_service))


if __name__ == "__main__":
    main()
