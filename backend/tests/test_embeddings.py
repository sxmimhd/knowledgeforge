from app.services.embeddings.service import EmbeddingService
from app.services.embeddings.search import SemanticSearch


documents = [
    "KnowledgeForge is an AI knowledge platform.",
    "Users can upload documents to their workspace.",
    "PDF files can be processed and converted into text.",
    "The system uses embeddings for semantic search.",
    "Qdrant stores vector embeddings for retrieval.",
    "Python is a popular programming language.",
    "The weather today is sunny and warm.",
    "A neural network consists of layers of connected neurons.",
]


def main():
    print("\nLoading embedding model...\n")

    embedding_service = EmbeddingService()

    print("\nCreating semantic search engine...\n")

    search_engine = SemanticSearch(embedding_service)

    search_engine.add_documents(documents)

    queries = [
        "How does KnowledgeForge find relevant information?",
        "How are uploaded PDF documents handled?",
        "What is the weather like?",
        "What stores vector embeddings?",
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        results = search_engine.search(
            query,
            top_k=3,
        )

        for index, result in enumerate(results, start=1):
            print(
                f"\n{index}. Score: {result['score']:.4f}"
            )
            print(f"   {result['text']}")


if __name__ == "__main__":
    main()