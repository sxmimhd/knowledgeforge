from app.services.embeddings.search import SemanticSearch


DOCUMENTS = [
    {
        "text": "KnowledgeForge is an AI knowledge platform.",
        "metadata": {
            "source": "knowledgeforge.txt",
            "document_type": "txt",
        },
    },
    {
        "text": "PDF files can be processed and converted into text.",
        "metadata": {
            "source": "document-processing.txt",
            "document_type": "txt",
        },
    },
    {
        "text": "Qdrant stores vector embeddings for retrieval.",
        "metadata": {
            "source": "qdrant-guide.txt",
            "document_type": "txt",
        },
    },
    {
        "text": "Python is a popular programming language.",
        "metadata": {
            "source": "python.txt",
            "document_type": "txt",
        },
    },
    {
        "text": "The weather today is sunny and warm.",
        "metadata": {
            "source": "weather.txt",
            "document_type": "txt",
        },
    },
]


def main():
    print("Creating Qdrant semantic search...")

    search = SemanticSearch(
        collection_name="knowledgeforge_semantic_test",
    )

    print("Adding documents...")

    search.add_documents(DOCUMENTS)

    print(f"Documents stored: {search.count()}")

    queries = [
        "How does KnowledgeForge work?",
        "What stores vector embeddings?",
        "What is the weather like?",
    ]

    for query in queries:
        print(f"\nQUERY: {query}")

        results = search.search(
            query=query,
            top_k=3,
        )

        for index, result in enumerate(results, start=1):
            print(f"{index}. Score: {result['score']:.4f}")
            print(
                f"   Source: "
                f"{result['metadata']['source']}"
            )
            print(f"   Text: {result['text']}")


if __name__ == "__main__":
    main()