# KnowledgeForge

**An enterprise-oriented RAG knowledge platform powered by local AI.**

KnowledgeForge transforms documents into searchable knowledge and lets users ask questions grounded in their own information. It combines document ingestion, semantic retrieval, vector search, and locally hosted LLM inference in a FastAPI backend.

## Core Features

- **Document ingestion:** Upload `.txt`, `.md`, and `.pdf` documents.
- **Document processing:** Extract, clean, and split document content into overlapping chunks.
- **Local embeddings:** Generate 384-dimensional embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector search:** Store and retrieve document chunks using Qdrant.
- **Retrieval-Augmented Generation:** Supply relevant retrieved context to a local language model before generating answers.
- **Streaming responses:** Deliver generated answers through Server-Sent Events (SSE).
- **Source attribution:** Return retrieved source metadata and include citation references in generated answers.
- **Workspace isolation:** Associate documents and retrieval operations with individual workspaces.
- **Document management:** List uploaded documents, reject unsupported or empty files, detect duplicate content, and delete documents.
- **Persistent storage:** Use PostgreSQL for workspace and document metadata, and persistent Docker volumes for infrastructure data.

## Architecture

```text
                  KnowledgeForge
                         |
                 FastAPI Application
                         |
             +-----------+-----------+
             |                       |
       Workspace API            RAG API
             |                       |
       Document Upload          User Query
             |                       |
       Text Extraction          Embedding
             |                       |
         Chunking              Qdrant Search
             |                       |
         Embeddings             Retrieved Context
             |                       |
          Qdrant                 Local LLM
                                     |
                               Token Streaming
                                     |
                             Answer + Sources
```

## Technology Stack

| Component | Technology |
|---|---|
| Backend API | Python, FastAPI |
| Validation and configuration | Pydantic / Pydantic Settings |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Vector database | Qdrant |
| Embedding model | Sentence Transformers, MiniLM-L6-v2 |
| LLM inference | Ollama |
| Language model | Qwen2.5-Coder 7B |
| API streaming | Server-Sent Events |
| Infrastructure | Docker |
| Testing | pytest, HTTPX |

## Project Structure

```text
KnowledgeForge/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│   ├── tests/
│   ├── pyproject.toml
│   └── .env
├── README.md
└── .gitignore
```

*The structure above summarizes the main components; keep it synchronized with the actual repository.*

## Getting Started

### Prerequisites

- Python 3.11 or newer
- `uv`
- Docker Desktop
- Ollama
- A locally available compatible language model

### 1. Start the infrastructure

Start the PostgreSQL and Qdrant containers configured for the project.

Ensure Ollama is running and the configured model is available locally.

### 2. Configure the backend

Create `backend/.env` using the project's environment configuration.

Example:

```env
DATABASE_URL=postgresql+pg8000://knowledgeforge:knowledgeforge@localhost:5432/knowledgeforge
```

Configure the remaining settings according to the application's actual configuration classes. Never commit real credentials or API keys.

### 3. Install dependencies

```powershell
cd backend
uv sync
```

If the project uses a separate development dependency group, install it according to the project's `uv` configuration.

### 4. Start the API

```powershell
uv run python -m uvicorn app.main:app
```

The API will be available at:

- API root: `http://127.0.0.1:8000/`
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

### 5. Run the tests

```powershell
uv run python -m pytest -v
```

## API Overview

| Operation | Endpoint |
|---|---|
| API health / root | `GET /` |
| Create workspace | `POST /api/v1/workspaces` |
| List workspace documents | `GET /api/v1/workspaces/{workspace_id}/documents` |
| Upload and ingest document | `POST /api/v1/workspaces/{workspace_id}/documents` |
| Delete document | `DELETE /api/v1/workspaces/{workspace_id}/documents/{document_id}` |
| Stream a RAG answer | `POST /api/v1/rag/stream` |

Check `/docs` for the precise request schemas and available endpoints.

## Streaming and Citations

The RAG streaming endpoint emits SSE events.

- `sources`: retrieved source metadata and the number of retrieved chunks.
- `token`: a generated text fragment.
- `done`: signals completion of the response.

This allows a client to render an answer incrementally while retaining the source information used to generate it.

## Testing and Verification

The workspace document test suite has passed five tests covering document listing, unsupported file types, empty uploads, duplicate upload rejection, and document deletion.

An end-to-end RAG verification also confirmed that KnowledgeForge could ingest a test document, retrieve its content, generate the expected answer using the local model, stream tokens, return source metadata, and delete the document afterward.

## Design Goals

KnowledgeForge is being developed around:

- Local inference to reduce dependence on external LLM APIs.
- Workspace-scoped retrieval to separate knowledge collections.
- Modular services for ingestion, embeddings, retrieval, and generation.
- Source-grounded answers rather than relying exclusively on model memory.
- A backend foundation that can support a richer knowledge-management interface.

