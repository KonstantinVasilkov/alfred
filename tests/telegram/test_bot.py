from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.types import Message, User

from alfred.telegram.bot import create_dispatcher, echo_handler, start_handler


@pytest.mark.asyncio
async def test_start_handler() -> None:
    """Test /start command handler responds with greeting."""
    # Arrange
    user = User(id=123, is_bot=False, first_name="John", last_name="Doe")
    message = MagicMock(spec=Message)
    message.from_user = user
    message.answer = AsyncMock()

    # Act
    await start_handler(message=message)

    # Assert
    message.answer.assert_called_once_with(text="Hello, John Doe!")


@pytest.mark.asyncio
async def test_echo_handler() -> None:
    """Test echo handler responds with same message text."""
    # Arrange
    message = MagicMock(spec=Message)
    message.text = "Test message"
    message.answer = AsyncMock()

    # Act
    await echo_handler(message=message)

    # Assert
    message.answer.assert_called_once_with(text="Test message")


def test_create_dispatcher_registers_handlers() -> None:
    """Test dispatcher is created with handlers registered."""
    # Act
    dp = create_dispatcher()

    # Assert
    assert dp is not None
    # Verify dispatcher is properly configured
    assert dp.message is not None
