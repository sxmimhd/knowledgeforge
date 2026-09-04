from typing import List, Dict, Any

from app.services.embeddings.service import EmbeddingService


class SemanticSearch:
    """
    Simple in-memory semantic search engine.

    This is intentionally NOT using Qdrant yet.
    We are learning the retrieval mechanics first.
    """

    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[str]) -> None:
        """
        Embed and store documents.
        """

        embeddings = self.embedding_service.embed_texts(documents)

        self.documents = [
            {
                "text": text,
                "embedding": embedding,
            }
            for text, embedding in zip(documents, embeddings)
        ]

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Find the most semantically similar documents.
        """

        if not self.documents:
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
                }
            )

        results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        return results[:top_k]