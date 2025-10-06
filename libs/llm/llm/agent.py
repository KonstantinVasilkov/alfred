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
