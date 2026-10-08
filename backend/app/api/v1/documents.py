import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document, Workspace
from app.services.documents.workspace_ingestion import (
    WorkspaceIngestionService,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Documents"],
)


ALLOWED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
}


@router.post("/{workspace_id}/documents")
async def upload_document(
    workspace_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    workspace = db.get(
        Workspace,
        workspace_id,
    )

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found.",
        )

    filename = file.filename or "unknown"

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Supported types: {sorted(ALLOWED_EXTENSIONS)}"
            ),
        )

    document = Document(
        workspace_id=workspace_id,
        filename=filename,
        file_type=extension.lstrip("."),
        source=filename,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        with NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

            temp_path = temp_file.name

        ingestion = WorkspaceIngestionService()

        result = ingestion.ingest(
            file_path=temp_path,
            workspace_id=workspace_id,
            document_id=document.id,
        )

        Path(temp_path).unlink(
            missing_ok=True,
        )

        return {
            "status": "completed",
            "document": {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "workspace_id": workspace_id,
            },
            "ingestion": result,
        }

    except Exception:
        db.delete(document)
        db.commit()

        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed.",
        )