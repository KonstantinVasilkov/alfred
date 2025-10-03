import asyncio

from alfred.config import get_settings
from alfred.telegram.bot import run_bot


def main() -> None:
    """Entry point for the application."""
    settings = get_settings()
    asyncio.run(run_bot(token=settings.telegram_bot_token))


if __name__ == "__main__":
    main()
