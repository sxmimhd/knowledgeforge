from typing import Any

from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.qdrant import QdrantVectorStore


class RetrievalService:
    def __init__(
        self,
        embeddings: EmbeddingService | None = None,
        vector_store: QdrantVectorStore | None = None,
    ):
        self.embeddings = embeddings or EmbeddingService()
        self.vector_store = vector_store or QdrantVectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        workspace_id: str | None = None,
        min_score: float = 0.25,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            return []

        query_vector = self.embeddings.embed_text(query)

        filters = dict(metadata_filter or {})
        if workspace_id:
            filters["workspace_id"] = workspace_id

        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            metadata_filter=filters or None,
        )

        return [
            result for result in results
            if result.get("score", 0.0) >= min_score
        ]
    def build_context(
        self,
        results: list[dict[str, Any]],
    ) -> str:
        if not results:
            return "No relevant information was found."

        context_parts = []

        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})

            source = metadata.get(
                "filename",
                metadata.get("source", "unknown"),
            )

            context_parts.append(
                f"[Source {index}: {source}]\n"
                f"{result.get('text', '')}"
            )

        return "\n\n".join(context_parts)