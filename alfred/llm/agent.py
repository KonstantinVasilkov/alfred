from abc import ABC, abstractmethod

from alfred.config import Settings


class LLMAgent(ABC):
    """Abstract base class for LLM agents."""

    @abstractmethod
    async def process_message(self, text: str) -> str:
        """Process a text message and return LLM response.

        Args:
            text: Input text to process

        Returns:
            Generated response text
        """
        pass


def create_agent(settings: Settings) -> LLMAgent:
    """Factory function to create LLM agent based on configuration.

    Args:
        settings: Application settings

    Returns:
        Configured LLM agent instance
    """
    from alfred.llm.anthropic_agent import AnthropicAgent

    return AnthropicAgent(api_key=settings.ANTHROPIC_API_KEY, model=settings.LLM_MODEL)
