from pathlib import Path

from app.services.documents.chunker import DocumentChunker
from app.services.documents.extractor import DocumentExtractor


FIXTURES = Path(__file__).parent / "fixtures"


def main():
    extractor = DocumentExtractor()
    chunker = DocumentChunker(
        chunk_size=150,
        chunk_overlap=30,
    )

    result = extractor.extract(FIXTURES / "sample.txt")

    chunks = chunker.chunk(
        text=result["text"],
        metadata=result["metadata"],
    )

    print("=" * 60)
    print("KnowledgeForge Chunking Test")
    print("=" * 60)

    print(f"\nOriginal characters: {len(result['text'])}")
    print(f"Chunks created: {len(chunks)}")

    for chunk in chunks:
        print("\n" + "-" * 40)
        print(f"Chunk index: {chunk['metadata']['chunk_index']}")
        print(
            f"Characters: "
            f"{chunk['metadata']['start_char']}"
            f" -> "
            f"{chunk['metadata']['end_char']}"
        )
        print(chunk["text"])

    print("\n" + "=" * 60)
    print("Chunking test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()