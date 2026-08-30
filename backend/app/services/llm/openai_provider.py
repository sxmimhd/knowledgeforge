from openai import AsyncOpenAI

from app.core.config import settings
from app.services.llm.base import BaseLLM


class OpenAIProvider(BaseLLM):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content or ""