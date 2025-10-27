from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram_bot.message_service import MessageService

# Global message service instance (will be initialized in run_bot)
_message_service: MessageService | None = None


async def start_handler(message: Message) -> None:
    """Handle /start command."""
    if message.from_user is None:
        return
    await message.answer(text=f"Hello, {message.from_user.full_name}!")


async def message_handler(message: Message) -> None:
    """Process user message through LLM and respond."""
    if message.text is None:
        return

    if _message_service is None:
        await message.answer(text="Bot is not properly configured. Please try again later.")
        return

    # Show typing indicator while processing
    if message.bot is not None:
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    response = await _message_service.process_user_message(message_text=message.text)
    await message.answer(text=response)


def create_bot(token: str) -> Bot:
    """Create and configure bot instance."""
    return Bot(token=token)


def create_dispatcher() -> Dispatcher:
    """Create and configure dispatcher with handlers."""
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(message_handler)

    return dp


async def run_bot(token: str, message_service: MessageService) -> None:
    """Run the bot.

    Args:
        token: Telegram bot token
        message_service: Message service instance for LLM processing

    """
    global _message_service
    _message_service = message_service

    bot = create_bot(token=token)
    dp = create_dispatcher()

    await dp.start_polling(bot)
