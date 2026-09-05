from app.services.embeddings.service import EmbeddingService
from app.services.embeddings.search import SemanticSearch


documents = [
    {
        "text": "KnowledgeForge is an AI knowledge platform.",
        "metadata": {
            "document_id": "doc_001",
            "filename": "knowledgeforge.txt",
        },
    },
    {
        "text": "Users can upload documents to their workspace.",
        "metadata": {
            "document_id": "doc_002",
            "filename": "workspace-guide.txt",
        },
    },
    {
        "text": "PDF files can be processed and converted into text.",
        "metadata": {
            "document_id": "doc_003",
            "filename": "document-processing.txt",
        },
    },
    {
        "text": "The system uses embeddings for semantic search.",
        "metadata": {
            "document_id": "doc_004",
            "filename": "search-guide.txt",
        },
    },
    {
        "text": "Qdrant stores vector embeddings for retrieval.",
        "metadata": {
            "document_id": "doc_005",
            "filename": "qdrant-guide.txt",
        },
    },
    {
        "text": "Python is a popular programming language.",
        "metadata": {
            "document_id": "doc_006",
            "filename": "python.txt",
        },
    },
    {
        "text": "The weather today is sunny and warm.",
        "metadata": {
            "document_id": "doc_007",
            "filename": "weather.txt",
        },
    },
    {
        "text": "A neural network consists of layers of connected neurons.",
        "metadata": {
            "document_id": "doc_008",
            "filename": "neural-networks.txt",
        },
    },
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

            print(
                f"   Source: "
                f"{result['metadata'].get('filename', 'unknown')}"
            )

            print(f"   {result['text']}")


if __name__ == "__main__":
    main()