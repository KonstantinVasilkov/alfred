from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """Request model for LLM processing."""

    text: str = Field(description="Input text to process")


class LLMResponse(BaseModel):
    """Response model from LLM processing."""

    text: str = Field(description="Generated response text")
