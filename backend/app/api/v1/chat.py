from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.chat.dependencies import get_chat_service
from app.services.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    if request.stream:

        async def generate():
            async for chunk in chat_service.stream(request):
                yield chunk

        return StreamingResponse(
            generate(),
            media_type="text/plain",
        )

    response = await chat_service.generate(request)

    return {
        "success": True,
        "message": "Response generated successfully",
        "data": {
            "response": response,
        },
    }