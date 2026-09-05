from typing import List, Dict, Any

from app.services.embeddings.service import EmbeddingService


class SemanticSearch:
    """
    In-memory semantic search engine.

    This is intentionally kept separate from the vector database.
    Qdrant will replace this storage/retrieval layer in Module 3.
    """

    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.documents: List[Dict[str, Any]] = []

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
    ) -> None:
        """
        Add documents and generate their embeddings.

        Each document should contain:
            {
                "text": "...",
                "metadata": {...}
            }
        """

        texts = [
            document["text"]
            for document in documents
        ]

        embeddings = self.embedding_service.embed_texts(texts)

        self.documents = [
            {
                "text": document["text"],
                "metadata": document.get("metadata", {}),
                "embedding": embedding,
            }
            for document, embedding in zip(documents, embeddings)
        ]

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most semantically similar documents.
        """

        if not self.documents:
            return []

        if top_k <= 0:
            return []

        query_embedding = self.embedding_service.embed_text(query)

        results = []

        for document in self.documents:
            score = self.embedding_service.cosine_similarity(
                query_embedding,
                document["embedding"],
            )

            results.append(
                {
                    "text": document["text"],
                    "score": score,
                    "metadata": document["metadata"],
                }
            )

        results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        return results[:top_k]