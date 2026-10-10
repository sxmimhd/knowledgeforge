from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch
from app.db.database import get_db
client = TestClient(app)

WORKSPACE_ID = "634c845b-ecb3-4055-a95b-3205b70f493d"


def test_list_workspace_documents():
    response = client.get(
        f"/api/v1/workspaces/{WORKSPACE_ID}/documents"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["workspace_id"] == WORKSPACE_ID
    assert "documents" in data
    assert "count" in data


def test_upload_rejects_unsupported_file_type():
    response = client.post(
        f"/api/v1/workspaces/{WORKSPACE_ID}/documents",
        files={"file": ("malware.exe", b"test content")},
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upload_rejects_empty_file():
    response = client.post(
        f"/api/v1/workspaces/{WORKSPACE_ID}/documents",
        files={"file": ("empty.txt", b"")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty."


def test_duplicate_upload_returns_conflict():
    db = MagicMock()
    db.get.return_value = MagicMock()

    existing_document = MagicMock()
    existing_document.id = "existing-document-id"
    existing_document.filename = "sample.md"
    db.scalar.return_value = existing_document

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.post(
            f"/api/v1/workspaces/{WORKSPACE_ID}/documents",
            files={"file": ("sample.md", b"duplicate content")},
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]["message"]
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_delete_document():
    db = MagicMock()
    document = MagicMock()
    document.id = "test-document-id"
    document.workspace_id = WORKSPACE_ID
    db.scalar.return_value = document

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch("app.api.v1.documents.QdrantVectorStore") as vector_store:
            response = client.delete(
                f"/api/v1/workspaces/{WORKSPACE_ID}/documents/test-document-id"
            )

        assert response.status_code == 200
        assert response.json()["status"] == "deleted"
        db.delete.assert_called_once_with(document)
        db.commit.assert_called_once()
        vector_store.return_value.delete_document.assert_called_once_with(
            "test-document-id"
        )
    finally:
        app.dependency_overrides.pop(get_db, None)
