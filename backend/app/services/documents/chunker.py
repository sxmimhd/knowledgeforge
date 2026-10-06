from typing import Any


class DocumentChunker:
    """
    Splits extracted document text into overlapping chunks.

    Defaults:
    - 800 characters per chunk
    - 120 characters overlap
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 120,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        text = text.strip()

        if not text:
            return []

        metadata = metadata or {}

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": {
                            **metadata,
                            "chunk_index": chunk_index,
                            "start_char": start,
                            "end_char": end,
                        },
                    }
                )

                chunk_index += 1

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        return chunks