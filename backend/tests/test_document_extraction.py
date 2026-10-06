from pathlib import Path

from app.services.documents.extractor import DocumentExtractor


FIXTURES = Path(__file__).parent / "fixtures"


def main():
    extractor = DocumentExtractor()

    print("=" * 60)
    print("KnowledgeForge Document Extraction Test")
    print("=" * 60)

    for filename in ["sample.txt", "sample.md"]:
        path = FIXTURES / filename

        result = extractor.extract(path)

        print(f"\nFILE: {filename}")
        print(f"TYPE: {result['metadata']['file_type']}")
        print(f"TEXT LENGTH: {len(result['text'])}")
        print("-" * 40)
        print(result["text"][:500])

    print("\n" + "=" * 60)
    print("Extraction test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()