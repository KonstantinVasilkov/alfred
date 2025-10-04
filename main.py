import asyncio

from alfred.config import get_settings
from alfred.llm.agent import create_agent
from alfred.services.message_service import MessageService
from alfred.telegram.bot import run_bot


def main() -> None:
    """Entry point for the application."""
    settings = get_settings()

    # Create LLM agent and message service
    llm_agent = create_agent(settings=settings)
    message_service = MessageService(llm_agent=llm_agent)

    # Run the bot
    asyncio.run(run_bot(token=settings.telegram_bot_token, message_service=message_service))


if __name__ == "__main__":
    main()
