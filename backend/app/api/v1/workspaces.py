from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Workspace


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


@router.post("")
def create_workspace(
    request: WorkspaceCreate,
    db: Session = Depends(get_db),
):
    workspace = Workspace(
        name=request.name.strip(),
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return {
        "id": workspace.id,
        "name": workspace.name,
        "created_at": workspace.created_at,
    }


@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: str,
    db: Session = Depends(get_db),
):
    workspace = db.get(Workspace, workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found.",
        )

    return {
        "id": workspace.id,
        "name": workspace.name,
        "created_at": workspace.created_at,
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "source": document.source,
                "created_at": document.created_at,
            }
            for document in workspace.documents
        ],
    }