from pydantic_ai import Agent

from alfred.llm.agent import LLMAgent


class AnthropicAgent(LLMAgent):
    """Anthropic-specific LLM agent implementation using pydantic-ai."""

    def __init__(self, api_key: str, model: str) -> None:
        """Initialize Anthropic agent.

        Args:
            api_key: Anthropic API key
            model: Model name to use (e.g., 'claude-3-haiku-20240307')
        """
        self._agent: Agent[None, str] = Agent(
            model=model,
            system_prompt="You are a helpful assistant. Provide concise and accurate responses.",
        )
        self._api_key = api_key

    async def process_message(self, text: str) -> str:
        """Process a text message using Anthropic's Claude model.

        Args:
            text: Input text to process

        Returns:
            Generated response text
        """
        result = await self._agent.run(user_prompt=text)
        return str(result.data)  # type: ignore[attr-defined]
