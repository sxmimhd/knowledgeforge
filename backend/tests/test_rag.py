import asyncio

from app.services.documents.ingestion import DocumentIngestionService
from app.services.rag.service import RAGService


DOCUMENTS = "tests/fixtures/documents"


async def main():
    print("=" * 60)
    print("KnowledgeForge RAG Generation Test")
    print("=" * 60)

    print("\n1. Ingesting documents...")

    ingestion = DocumentIngestionService()

    results = ingestion.ingest_directory(DOCUMENTS)

    for result in results:
        print(
            f"  {result['filename']}"
            f" | chunks={result['chunks']}"
            f" | vectors={result['vectors']}"
        )

    print("\n2. Initializing RAG service...")

    rag = RAGService()

    queries = [
        "What is KnowledgeForge?",
        "Which technology stores the vectors?",
        "Which language model system is used?",
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print(f"QUESTION: {query}")
        print("=" * 60)

        result = await rag.generate(
            query=query,
            top_k=3,
        )

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(
                f"  - {source['filename']}"
                f" | score={source['score']:.4f}"
            )

        print(
            f"\nRetrieved chunks: "
            f"{result['retrieved_chunks']}"
        )

    print("\n" + "=" * 60)
    print("RAG GENERATION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())