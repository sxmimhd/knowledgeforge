from pathlib import Path
from typing import Any

from app.services.documents.chunker import DocumentChunker
from app.services.documents.extractor import DocumentExtractor
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.qdrant import QdrantVectorStore


class DocumentIngestionService:
    """
    Document ingestion pipeline:

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

    def ingest_file(
        self,
        file_path: str | Path,
    ) -> dict[str, Any]:

        document = self.extractor.extract(file_path)

        chunks = self.chunker.chunk(
            text=document["text"],
            metadata=document["metadata"],
        )

        if not chunks:
            raise ValueError(
                f"No chunks generated from {file_path}"
            )

        texts = [chunk["text"] for chunk in chunks]

        vectors = self.embeddings.embed_texts(texts)

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
        }

    def ingest_files(
        self,
        file_paths: list[str | Path],
    ) -> list[dict[str, Any]]:

        results = []

        for file_path in file_paths:
            result = self.ingest_file(file_path)
            results.append(result)

        return results

    def ingest_directory(
        self,
        directory: str | Path,
    ) -> list[dict[str, Any]]:

        directory = Path(directory)

        if not directory.exists():
            raise ValueError(
                f"Directory does not exist: {directory}"
            )

        files = [
            path
            for path in directory.iterdir()
            if path.is_file()
            and path.suffix.lower()
            in self.extractor.SUPPORTED_EXTENSIONS
        ]

        return self.ingest_files(files)