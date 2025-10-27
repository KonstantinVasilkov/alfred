import time

from llm.agent import LLMAgent
from shared_infra import get_logger


class MessageService:
    """Service layer for message processing orchestration."""

    def __init__(self, llm_agent: LLMAgent) -> None:
        """Initialize message service.

        Args:
            llm_agent: LLM agent instance for processing messages

        """
        self._llm_agent = llm_agent
        self._logger = get_logger(__name__)

    async def process_user_message(self, message_text: str) -> str:
        """Process user message through LLM and return response.

        Args:
            message_text: User's input message

        Returns:
            LLM-generated response

        """
        start_time = time.time()
        self._logger.info(
            "llm_processing_started",
            message_length=len(message_text),
            message_preview=message_text[:100],
        )

        try:
            response = await self._llm_agent.process_message(text=message_text)
            processing_time = time.time() - start_time

            self._logger.info(
                "llm_processing_completed",
                processing_time_seconds=round(processing_time, 2),
                response_length=len(response),
            )

            return response

        except Exception as e:
            processing_time = time.time() - start_time
            error_type = type(e).__name__

            self._logger.exception(
                "llm_processing_failed",
                error_type=error_type,
                processing_time_seconds=round(processing_time, 2),
                message_preview=message_text[:100],
                extra={"sentry_fingerprint": ["llm-processing-failed", error_type]},
            )

            return f"Sorry, I encountered an error processing your message: {e!s}"
