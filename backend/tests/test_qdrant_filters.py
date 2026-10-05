from app.services.embeddings.search import SemanticSearch


DOCUMENTS = [
    {
        "text": "Alpha company employees receive 20 vacation days per year.",
        "metadata": {
            "workspace_id": "workspace_alpha",
            "source": "alpha-handbook.pdf",
        },
    },
    {
        "text": "Alpha company employees receive free technical training.",
        "metadata": {
            "workspace_id": "workspace_alpha",
            "source": "alpha-benefits.pdf",
        },
    },
    {
        "text": "Beta company employees receive 30 vacation days per year.",
        "metadata": {
            "workspace_id": "workspace_beta",
            "source": "beta-handbook.pdf",
        },
    },
    {
        "text": "Beta company provides transportation benefits.",
        "metadata": {
            "workspace_id": "workspace_beta",
            "source": "beta-benefits.pdf",
        },
    },
]


def main():
    search = SemanticSearch(
        collection_name="knowledgeforge_filter_test",
    )

    print("Adding documents...")
    search.add_documents(DOCUMENTS)

    print(f"Stored documents: {search.count()}")

    query = "How many vacation days do employees receive?"

    print("\n=== WITHOUT FILTER ===")

    results = search.search(
        query=query,
        top_k=4,
    )

    for result in results:
        print(
            f"{result['score']:.4f} | "
            f"{result['metadata']['workspace_id']} | "
            f"{result['text']}"
        )

    print("\n=== ALPHA WORKSPACE ONLY ===")

    results = search.search(
        query=query,
        top_k=4,
        metadata_filter={
            "workspace_id": "workspace_alpha",
        },
    )

    for result in results:
        print(
            f"{result['score']:.4f} | "
            f"{result['metadata']['workspace_id']} | "
            f"{result['text']}"
        )

    print("\n=== BETA WORKSPACE ONLY ===")

    results = search.search(
        query=query,
        top_k=4,
        metadata_filter={
            "workspace_id": "workspace_beta",
        },
    )

    for result in results:
        print(
            f"{result['score']:.4f} | "
            f"{result['metadata']['workspace_id']} | "
            f"{result['text']}"
        )


if __name__ == "__main__":
    main()