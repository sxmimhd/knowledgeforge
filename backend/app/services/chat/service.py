from collections.abc import AsyncIterator

from app.schemas.chat import ChatRequest
from app.services.llm.base import BaseLLM


class ChatService:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def build_messages(
        self,
        request: ChatRequest,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": request.system_prompt,
            }
        ]

        messages.extend(
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        )

        messages.append(
            {
                "role": "user",
                "content": request.message,
            }
        )

        return messages

    async def generate(
        self,
        request: ChatRequest,
    ) -> str:
        messages = self.build_messages(request)

        return await self.llm.generate(
            messages=messages,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
        )

    async def stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        messages = self.build_messages(request)

        async for chunk in self.llm.stream(
            messages=messages,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
        ):
            yield chunk