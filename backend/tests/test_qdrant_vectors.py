from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.qdrant import QdrantVectorStore


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
    print("Loading embedding model...")

    embeddings = EmbeddingService()

    print("Connecting to Qdrant...")

    vector_store = QdrantVectorStore(
        collection_name="knowledgeforge_test"
    )

    print("Creating document embeddings...")

    vectors = embeddings.embed_texts(
        [document["text"] for document in DOCUMENTS]
    )

    print(f"Generated {len(vectors)} vectors.")
    print(f"Vector dimension: {len(vectors[0])}")

    print("\nStoring vectors in Qdrant...")

    vector_store.add_documents(
        documents=DOCUMENTS,
        vectors=vectors,
    )

    print(f"Stored vectors: {vector_store.count()}")

    queries = [
        "How does KnowledgeForge work?",
        "What stores vector embeddings?",
        "What is the weather like?",
    ]

    for query in queries:
        print(f"\nQUERY: {query}")

        query_vector = embeddings.embed_text(query)

        results = vector_store.search(
            query_vector=query_vector,
            top_k=3,
        )

        for index, result in enumerate(results, start=1):
            print(f"{index}. Score: {result['score']:.4f}")
            print(f"   Source: {result['metadata']['source']}")
            print(f"   Text: {result['text']}")


if __name__ == "__main__":
    main()