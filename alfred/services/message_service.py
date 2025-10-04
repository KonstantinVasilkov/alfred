from alfred.llm.agent import LLMAgent


class MessageService:
    """Service layer for message processing orchestration."""

    def __init__(self, llm_agent: LLMAgent) -> None:
        """Initialize message service.

        Args:
            llm_agent: LLM agent instance for processing messages
        """
        self._llm_agent = llm_agent

    async def process_user_message(self, message_text: str) -> str:
        """Process user message through LLM and return response.

        Args:
            message_text: User's input message

        Returns:
            LLM-generated response
        """
        try:
            response = await self._llm_agent.process_message(text=message_text)
            return response
        except Exception as e:
            # Log error and return user-friendly message
            # In production, add proper logging here
            return f"Sorry, I encountered an error processing your message: {str(e)}"
