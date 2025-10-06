from abc import ABC, abstractmethod


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


def create_agent(api_key: str, model: str) -> LLMAgent:
    """Factory function to create LLM agent based on configuration.

    Args:
        api_key: API key for the LLM provider
        model: Model identifier to use

    Returns:
        Configured LLM agent instance
    """
    from llm.anthropic_agent import AnthropicAgent

    return AnthropicAgent(api_key=api_key, model=model)
