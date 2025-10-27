"""Factory functions for creating LLM agents."""

from llm.agent import LLMAgent
from llm.anthropic_agent import AnthropicAgent


def create_agent(api_key: str, model: str) -> LLMAgent:
    """Create LLM agent based on configuration.

    Args:
        api_key: API key for the LLM provider
        model: Model identifier to use

    Returns:
        Configured LLM agent instance

    """
    return AnthropicAgent(api_key=api_key, model=model)
