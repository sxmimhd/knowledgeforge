from pathlib import Path
from typing import Any

from app.services.documents.chunker import DocumentChunker
from app.services.documents.extractor import DocumentExtractor
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.qdrant import QdrantVectorStore


class DocumentIngestionService:
    """
    Complete local document ingestion pipeline.

    File
      -> extraction
      -> chunking
      -> embeddings
      -> Qdrant
    """

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

    def ingest_file(self, file_path: str | Path) -> dict[str, Any]:
        # 1. Extract
        document = self.extractor.extract(file_path)

        # 2. Chunk
        chunks = self.chunker.chunk(
            text=document["text"],
            metadata=document["metadata"],
        )

        if not chunks:
            raise ValueError(
                f"No chunks generated from {file_path}"
            )

        # 3. Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        vectors = self.embeddings.embed_texts(texts)

        # 4. Store in Qdrant
        self.vector_store.add_documents(
            documents=chunks,
            vectors=vectors,
        )

        return {
            "filename": document["metadata"]["filename"],
            "file_type": document["metadata"]["file_type"],
            "characters": len(document["text"]),
            "chunks": len(chunks),
            "vectors": len(vectors),
            "qdrant_count": self.vector_store.count(),
        }