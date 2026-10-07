from pathlib import Path

from app.services.documents.ingestion import DocumentIngestionService


DOCUMENTS = Path(__file__).parent / "fixtures" / "documents"


def main():
    print("=" * 60)
    print("KnowledgeForge Ingested Knowledge Retrieval")
    print("=" * 60)

    service = DocumentIngestionService()

    print("\nIngesting documents...")

    service.ingest_directory(DOCUMENTS)

    print(
        f"Qdrant contains "
        f"{service.vector_store.count()} points."
    )

    queries = [
        "What is KnowledgeForge?",
        "Which technology stores the vectors?",
        "Which language model system is used?",
    ]

    for query in queries:
        print("\n" + "-" * 60)
        print(f"QUERY: {query}")
        print("-" * 60)

        query_vector = service.embeddings.embed_text(query)

        results = service.vector_store.search(
            query_vector=query_vector,
            top_k=3,
        )

        for index, result in enumerate(results, start=1):
            metadata = result["metadata"]

            print(
                f"\n#{index}"
                f" score={result['score']:.4f}"
                f" source={metadata.get('filename')}"
            )

            print(result["text"][:300])

    print("\n" + "=" * 60)
    print("RETRIEVAL TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()