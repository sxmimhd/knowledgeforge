from typing import Any

from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.qdrant import QdrantVectorStore


class SemanticSearch:
    def __init__(
        self,
        collection_name: str = "knowledgeforge",
    ):
        self.embedding_service = EmbeddingService()

        self.vector_store = QdrantVectorStore(
            collection_name=collection_name,
            vector_size=384,
        )

    def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> None:
        """
        Embed documents and store their vectors in Qdrant.
        """

        texts = [
            document["text"]
            for document in documents
        ]

        vectors = self.embedding_service.embed_texts(texts)

        self.vector_store.add_documents(
            documents=documents,
            vectors=vectors,
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """
        Convert the query into an embedding and
        retrieve the most semantically similar documents.
        """

        query_vector = self.embedding_service.embed_text(query)

        return self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )

    def count(self) -> int:
        return self.vector_store.count()