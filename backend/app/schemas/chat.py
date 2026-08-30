from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="The user's message.",
    )

    system_prompt: str = Field(
        default="You are KnowledgeForge, a helpful AI assistant.",
        description="System instructions for the model.",
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Controls randomness.",
    )

    top_p: float = Field(
        default=0.9,
        gt=0.0,
        le=1.0,
        description="Controls nucleus sampling.",
    )

    max_tokens: int = Field(
        default=500,
        ge=1,
        le=8192,
        description="Maximum generated tokens.",
    )

    history: list[ChatMessage] = Field(
        default_factory=list,
        description="Previous conversation messages.",
    )

    stream: bool = Field(
        default=False,
        description="Whether to stream the response.",
    )