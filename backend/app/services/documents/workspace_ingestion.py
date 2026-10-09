from pathlib import Path
from typing import Any

from app.services.documents.extractor import DocumentExtractor
from app.services.documents.chunker import DocumentChunker
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.qdrant import QdrantVectorStore


class WorkspaceIngestionService:
    def __init__(
        self,
        extractor: DocumentExtractor | None = None,
        chunker: DocumentChunker | None = None,
        embeddings: EmbeddingService | None = None,
        vector_store: QdrantVectorStore | None = None,
    ):
        self.extractor = extractor or DocumentExtractor()
        self.chunker = chunker or DocumentChunker()
        self.embeddings = embeddings or EmbeddingService()
        self.vector_store = vector_store or QdrantVectorStore()

    def ingest(
        self,
        file_path: str,
        workspace_id: str,
        document_id: str,
        original_filename: str | None = None,
    ) -> dict[str, Any]:

        path = Path(file_path)

        extracted = self.extractor.extract(path)
        display_filename = original_filename or path.name
        extracted["metadata"]["filename"] = original_filename or path.name
        extracted["metadata"]["source"] = original_filename or path.name

        chunks = self.chunker.chunk(
            extracted["text"],
        )

        documents = []

        for index, chunk in enumerate(chunks):
            documents.append(
                {
                    "text": chunk["text"],
                    "metadata": {
                        **extracted["metadata"],
                        "workspace_id": workspace_id,
                        "document_id": document_id,
                        "chunk_index": index,
                    },
                }
            )

        texts = [
            document["text"]
            for document in documents
        ]

        vectors = self.embeddings.embed_texts(texts)

        self.vector_store.add_documents(
            documents=documents,
            vectors=vectors,
            workspace_id=workspace_id,
        )

        return {
            "document_id": document_id,
            "workspace_id": workspace_id,
            "filename": display_filename,
            "file_type": path.suffix.lower(),
            "characters": len(extracted["text"]),
            "chunks": len(chunks),
            "vectors": len(vectors),
        }