
import hashlib
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document, Workspace
from app.services.documents.workspace_ingestion import WorkspaceIngestionService
from app.services.vector_store.qdrant import QdrantVectorStore

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workspaces", tags=["Documents"])

ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}


@router.post("/{workspace_id}/documents")
async def upload_document(
    workspace_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    workspace = db.get(Workspace, workspace_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    filename = Path(file.filename or "unknown").name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}. "
                   f"Supported types: {sorted(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    content_hash = hashlib.sha256(content).hexdigest()

    existing = db.scalar(
        select(Document).where(
            Document.workspace_id == workspace_id,
            Document.content_hash == content_hash,
        )
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "This file already exists in this workspace.",
                "document_id": existing.id,
                "filename": existing.filename,
            },
        )

    document = Document(
        workspace_id=workspace_id,
        filename=filename,
        file_type=extension.lstrip("."),
        source=filename,
        content_hash=content_hash,
    )

    temp_path = None

    try:
        db.add(document)
        db.commit()
        db.refresh(document)

        with NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        ingestion = WorkspaceIngestionService()
        result = ingestion.ingest(
            file_path=temp_path,
            workspace_id=workspace_id,
            document_id=document.id,
            original_filename=filename,
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

    except Exception as exc:
        logger.exception("Document ingestion failed")
        db.rollback()

        saved_document = db.get(Document, document.id)
        if saved_document is not None:
            db.delete(saved_document)
            db.commit()

        # Best-effort cleanup if ingestion wrote vectors before failing.
        try:
            QdrantVectorStore().delete_document(document.id)
        except Exception:
            logger.exception("Could not clean up partial document vectors")

        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed. Check the API logs.",
        ) from exc

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
        await file.close()


@router.get("/{workspace_id}/documents")
def list_documents(
    workspace_id: str,
    db: Session = Depends(get_db),
):
    workspace = db.get(Workspace, workspace_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    documents = db.scalars(
        select(Document)
        .where(Document.workspace_id == workspace_id)
        .order_by(Document.created_at.desc())
    ).all()

    return {
        "workspace_id": workspace_id,
        "count": len(documents),
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "created_at": doc.created_at,
            }
            for doc in documents
        ],
    }


@router.delete("/{workspace_id}/documents/{document_id}")
def delete_document(
    workspace_id: str,
    document_id: str,
    db: Session = Depends(get_db),
):
    document = db.scalar(
        select(Document).where(
            Document.id == document_id,
            Document.workspace_id == workspace_id,
        )
    )

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        # Remove indexed chunks before deleting the PostgreSQL record.
        QdrantVectorStore().delete_document(document.id)
        db.delete(document)
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.exception("Document deletion failed")
        raise HTTPException(
            status_code=500,
            detail="Document deletion failed. Check the API logs.",
        ) from exc

    return {
        "status": "deleted",
        "document_id": document_id,
        "workspace_id": workspace_id,
    }
