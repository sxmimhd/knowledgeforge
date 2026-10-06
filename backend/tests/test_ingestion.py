from pathlib import Path

from app.services.documents.ingestion import DocumentIngestionService


FIXTURES = Path(__file__).parent / "fixtures"


def main():
    print("=" * 60)
    print("KnowledgeForge Document Ingestion Test")
    print("=" * 60)

    service = DocumentIngestionService()

    print("\nIngesting sample.txt...")

    result = service.ingest_file(
        FIXTURES / "sample.txt"
    )

    print("\nRESULT")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 60)
    print("FULL INGESTION PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()