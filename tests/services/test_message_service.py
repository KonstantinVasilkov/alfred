from unittest.mock import AsyncMock, MagicMock

import pytest

from alfred.services.message_service import MessageService


@pytest.mark.asyncio
async def test_message_service_process_user_message_success() -> None:
    """Test message service processes user message successfully."""
    # Arrange
    mock_agent = MagicMock()
    mock_agent.process_message = AsyncMock(return_value="Agent response")

    service = MessageService(llm_agent=mock_agent)

    # Act
    response = await service.process_user_message(message_text="Hello")

    # Assert
    assert response == "Agent response"
    mock_agent.process_message.assert_called_once_with(text="Hello")


@pytest.mark.asyncio
async def test_message_service_handles_agent_error() -> None:
    """Test message service handles LLM agent errors gracefully."""
    # Arrange
    mock_agent = MagicMock()
    mock_agent.process_message = AsyncMock(side_effect=Exception("API error"))

    service = MessageService(llm_agent=mock_agent)

    # Act
    response = await service.process_user_message(message_text="Hello")

    # Assert
    assert "error processing your message" in response.lower()
    assert "API error" in response
