from fastapi import APIRouter

from app.schemas.common import APIResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=APIResponse)
def health_check():
    return APIResponse(
        success=True,
        message="API is healthy",
        data={
            "service": "KnowledgeForge API"
        },
    )