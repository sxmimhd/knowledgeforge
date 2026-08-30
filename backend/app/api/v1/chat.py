from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest
from app.services.llm.base import BaseLLM
from app.services.llm.dependencies import get_llm

router = APIRouter()


@router.post("/")
async def chat(
    request: ChatRequest,
    llm: BaseLLM = Depends(get_llm),
):
    messages = [
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

    response = await llm.generate(
        messages=messages,
        temperature=request.temperature,
        top_p=request.top_p,
        max_tokens=request.max_tokens,
    )

    return {
        "success": True,
        "message": "Response generated successfully",
        "data": {
            "response": response,
        },
    }