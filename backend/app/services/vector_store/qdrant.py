from typing import Any
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)


class QdrantVectorStore:
    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection_name: str = "knowledgeforge",
        vector_size: int = 384,
    ):
        self.client = QdrantClient(
            url=url,
            prefer_grpc=False,
        )

        self.collection_name = collection_name
        self.vector_size = vector_size

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        if not self.client.collection_exists(
            self.collection_name
        ):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add_documents(
        self,
        documents: list[dict[str, Any]],
        vectors: list[list[float]],
        workspace_id: str | None = None,
    ) -> None:
        if len(documents) != len(vectors):
            raise ValueError(
                "Number of documents must match number of vectors."
            )

        points = []

        for document, vector in zip(documents, vectors):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "text": document["text"],
                        "metadata": {
                            **document.get("metadata", {}),
                            "workspace_id": workspace_id,
                        },
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        query_filter = None

        if metadata_filter:
            conditions = []

            for field, value in metadata_filter.items():
                conditions.append(
                    FieldCondition(
                        key=f"metadata.{field}",
                        match=MatchValue(value=value),
                    )
                )

            query_filter = Filter(must=conditions)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        ).points

        return [
            {
                "score": result.score,
                "text": result.payload.get("text", ""),
                "metadata": result.payload.get(
                    "metadata", {}
                ),
            }
            for result in results
        ]

    def count(self) -> int:
        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        return result.count