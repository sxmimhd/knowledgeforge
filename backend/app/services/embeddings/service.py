from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    """
    Converts text into semantic vector embeddings.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model_name = model_name

        self.device = "cuda"

        try:
            self.model = SentenceTransformer(
                model_name,
                device=self.device,
            )
        except Exception:
            print("CUDA unavailable. Falling back to CPU.")
            self.device = "cpu"

            self.model = SentenceTransformer(
                model_name,
                device=self.device,
            )

        self.dimension = self.model.get_embedding_dimension()

        print(
            f"Embedding model loaded: {self.model_name} "
            f"| device={self.device} "
            f"| dimension={self.dimension}"
        )

    def embed_text(self, text: str) -> List[float]:
        """
        Convert a single piece of text into an embedding vector.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple pieces of text into embedding vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=16,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    @staticmethod
    def cosine_similarity(
        vector_a: List[float],
        vector_b: List[float],
    ) -> float:
        """
        Calculate cosine similarity between two vectors.
        """

        a = np.array(vector_a)
        b = np.array(vector_b)

        denominator = np.linalg.norm(a) * np.linalg.norm(b)

        if denominator == 0:
            return 0.0

        return float(np.dot(a, b) / denominator)