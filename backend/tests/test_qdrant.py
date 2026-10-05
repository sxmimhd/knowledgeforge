from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "knowledgeforge_test"


def main():
    print("Connecting to Qdrant...")

    client = QdrantClient(url=QDRANT_URL)

    print("Connected successfully.")

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
        print("Removed existing test collection.")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )

    print(f"Created collection: {COLLECTION_NAME}")

    collections = client.get_collections()

    print("\nCollections:")

    for collection in collections.collections:
        print(f"- {collection.name}")


if __name__ == "__main__":
    main()