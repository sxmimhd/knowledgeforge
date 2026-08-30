import logging

from openai import AsyncOpenAI

from app.services.llm.base import BaseLLM

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLM):

    def __init__(
        self,
        client: AsyncOpenAI,
        model: str,
    ):
        self.client = client
        self.model = model

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 500,
    ) -> str:

        logger.info(
            "Sending request to Ollama: model=%s",
            self.model,
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""