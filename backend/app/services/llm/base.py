from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 500,
    ) -> str:
        pass