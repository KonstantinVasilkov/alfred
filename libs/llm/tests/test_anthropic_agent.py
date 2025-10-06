from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from llm.anthropic_agent import AnthropicAgent


@pytest.mark.asyncio
async def test_anthropic_agent_process_message() -> None:
    """Test Anthropic agent processes message successfully."""
    # Arrange
    mock_result = MagicMock()
    mock_result.data = "This is a test response"

    with patch("llm.anthropic_agent.Agent") as mock_agent_class:
        mock_agent_instance = MagicMock()
        mock_agent_instance.run = AsyncMock(return_value=mock_result)
        mock_agent_class.return_value = mock_agent_instance

        agent = AnthropicAgent(api_key="test_key", model="claude-3-haiku-20240307")

        # Act
        response = await agent.process_message(text="Hello, how are you?")

        # Assert
        assert response == "This is a test response"
        mock_agent_instance.run.assert_called_once_with(user_prompt="Hello, how are you?")


@pytest.mark.asyncio
async def test_anthropic_agent_initialization() -> None:
    """Test Anthropic agent initializes with correct parameters."""
    # Arrange & Act
    with patch("llm.anthropic_agent.Agent") as mock_agent_class:
        with patch.dict("os.environ", {}, clear=True):
            agent = AnthropicAgent(api_key="test_api_key", model="claude-3-haiku-20240307")

            # Assert
            assert agent._agent is not None
            mock_agent_class.assert_called_once_with(
                model="claude-3-haiku-20240307",
                system_prompt="You are a helpful assistant. Provide concise and accurate responses.",
            )
