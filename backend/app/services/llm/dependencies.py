from functools import lru_cache

from app.core.config import settings
from app.services.llm.base import BaseLLM
from app.services.llm.ollama_provider import OllamaProvider
from app.services.llm.openai_provider import OpenAIProvider


@lru_cache
def get_llm() -> BaseLLM:
    if settings.llm_provider.lower() == "ollama":
        return OllamaProvider()

    if settings.llm_provider.lower() == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )