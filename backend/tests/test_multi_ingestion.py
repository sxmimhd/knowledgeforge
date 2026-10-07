from pathlib import Path

from app.services.documents.ingestion import DocumentIngestionService


DOCUMENTS = Path(__file__).parent / "fixtures" / "documents"


def main():
    print("=" * 60)
    print("KnowledgeForge Multi-Document Ingestion")
    print("=" * 60)

    service = DocumentIngestionService()

    results = service.ingest_directory(DOCUMENTS)

    print("\nINGESTION RESULTS")
    print("-" * 60)

    total_chunks = 0
    total_vectors = 0

    for result in results:
        print(
            f"{result['filename']:20}"
            f" | type={result['file_type']:4}"
            f" | chars={result['characters']:4}"
            f" | chunks={result['chunks']:3}"
            f" | vectors={result['vectors']:3}"
        )

        total_chunks += result["chunks"]
        total_vectors += result["vectors"]

    print("-" * 60)
    print(f"Files: {len(results)}")
    print(f"Total chunks: {total_chunks}")
    print(f"Total vectors: {total_vectors}")
    print(f"Qdrant points: {service.vector_store.count()}")

    print("\n" + "=" * 60)
    print("MULTI-DOCUMENT INGESTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()