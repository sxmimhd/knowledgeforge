from fastapi import APIRouter, Depends

from app.schemas.common import APIResponse
from app.services.llm.base import BaseLLM
from app.services.llm.dependencies import get_llm

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=APIResponse)
async def chat(
    message: str,
    llm: BaseLLM = Depends(get_llm),
) -> APIResponse:
    response = await llm.generate(
        system_prompt="You are KnowledgeForge, a helpful AI assistant.",
        user_prompt=message,
    )

    return APIResponse(
        success=True,
        message="Response generated successfully",
        data={
            "response": response,
        },
    )