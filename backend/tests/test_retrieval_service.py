from app.services.documents.ingestion import DocumentIngestionService
from app.services.retrieval.retrieval import RetrievalService


DOCUMENTS = "tests/fixtures/documents"


def main():
    print("=" * 60)
    print("KnowledgeForge Retrieval Service Test")
    print("=" * 60)

    ingestion = DocumentIngestionService()

    print("\nIngesting documents...")
    ingestion.ingest_directory(DOCUMENTS)

    retrieval = RetrievalService()

    queries = [
        "What is KnowledgeForge?",
        "Which technology stores vectors?",
        "Which language model system is used?",
    ]

    for query in queries:
        print("\n" + "-" * 60)
        print(f"QUERY: {query}")
        print("-" * 60)

        results = retrieval.retrieve(
            query=query,
            top_k=3,
        )

        print(f"Retrieved documents: {len(results)}")

        for index, result in enumerate(results, start=1):
            print(
                f"\n#{index}"
                f" score={result['score']:.4f}"
                f" source={result['metadata'].get('filename')}"
            )
            print(result["text"][:500])

        print("\nCONTEXT")
        print("-" * 40)
        print(retrieval.build_context(results))

    print("\n" + "=" * 60)
    print("RETRIEVAL SERVICE TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()