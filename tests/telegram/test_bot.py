from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import Message, User

from alfred.telegram.bot import create_dispatcher, message_handler, start_handler


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
async def test_message_handler_with_service() -> None:
    """Test message handler processes message through service."""
    # Arrange
    message = MagicMock()
    message.text = "Test message"
    message.answer = AsyncMock()
    message.chat = MagicMock()
    message.chat.id = 123
    message.bot = MagicMock()
    message.bot.send_chat_action = AsyncMock()

    mock_service = MagicMock()
    mock_service.process_user_message = AsyncMock(return_value="LLM response")

    # Act
    with patch("alfred.telegram.bot._message_service", mock_service):
        await message_handler(message=message)

    # Assert
    message.bot.send_chat_action.assert_called_once_with(chat_id=123, action="typing")
    mock_service.process_user_message.assert_called_once_with(message_text="Test message")
    message.answer.assert_called_once_with(text="LLM response")


@pytest.mark.asyncio
async def test_message_handler_without_service() -> None:
    """Test message handler handles missing service gracefully."""
    # Arrange
    message = MagicMock(spec=Message)
    message.text = "Test message"
    message.answer = AsyncMock()

    # Act
    with patch("alfred.telegram.bot._message_service", None):
        await message_handler(message=message)

    # Assert
    message.answer.assert_called_once()
    call_text = message.answer.call_args[1]["text"]
    assert "not properly configured" in call_text.lower()


def test_create_dispatcher_registers_handlers() -> None:
    """Test dispatcher is created with handlers registered."""
    # Act
    dp = create_dispatcher()

    # Assert
    assert dp is not None
    # Verify dispatcher is properly configured
    assert dp.message is not None
