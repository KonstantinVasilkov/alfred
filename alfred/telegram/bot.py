from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


async def start_handler(message: Message) -> None:
    """Handle /start command."""
    await message.answer(text=f"Hello, {message.from_user.full_name}!")


async def echo_handler(message: Message) -> None:
    """Echo any message back to the user."""
    await message.answer(text=message.text)


def create_bot(token: str) -> Bot:
    """Create and configure bot instance."""
    return Bot(token=token)


def create_dispatcher() -> Dispatcher:
    """Create and configure dispatcher with handlers."""
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(echo_handler)

    return dp


async def run_bot(token: str) -> None:
    """Run the bot."""
    bot = create_bot(token=token)
    dp = create_dispatcher()

    await dp.start_polling(bot)
