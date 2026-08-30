from fastapi import Depends

from app.services.chat.service import ChatService
from app.services.llm.base import BaseLLM
from app.services.llm.dependencies import get_llm


def get_chat_service(
    llm: BaseLLM = Depends(get_llm),
) -> ChatService:
    return ChatService(llm)