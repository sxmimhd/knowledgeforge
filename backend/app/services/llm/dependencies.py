from openai import AsyncOpenAI

from app.core.config import settings
from app.services.llm.base import BaseLLM
from app.services.llm.ollama_provider import OllamaProvider


def get_llm() -> BaseLLM:
    client = AsyncOpenAI(
        base_url=settings.llm_base_url,
        api_key="ollama",
    )

    return OllamaProvider(
        client=client,
        model=settings.llm_model,
    )