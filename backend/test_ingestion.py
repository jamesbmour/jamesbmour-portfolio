"""
Test script to validate Qdrant ingestion and retrieval.
Checks collection status and runs sample queries.
"""
import argparse
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from config import config


def main(skip_query: bool = False):
    """
    Validate Qdrant collection and test retrieval.

    Args:
        skip_query: Skip running sample queries (saves API calls)
    """
    print("="*60)
    print("QDRANT INGESTION VALIDATION")
    print("="*60 + "\n")

    # Validate config
    config.validate()

    # Initialize Qdrant client
    print("Connecting to Qdrant...")
    client = QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
    )

    # Check collection exists
    collections = client.get_collections()
    collection_exists = any(
        col.name == config.COLLECTION_NAME
        for col in collections.collections
    )

    if not collection_exists:
        print(f"✗ Collection '{config.COLLECTION_NAME}' not found!")
        print("\nAvailable collections:")
        for col in collections.collections:
            print(f"  - {col.name}")
        print("\nRun 'python ingest.py' to create the collection.")
        return

    print(f"✓ Collection '{config.COLLECTION_NAME}' found")

    # Get collection info
    collection_info = client.get_collection(config.COLLECTION_NAME)
    print(f"\nCollection Stats:")
    print(f"  - Vectors: {collection_info.vectors_count}")
    print(f"  - Points: {collection_info.points_count}")

    # Get sample points to analyze sources
    print("\nFetching sample points...")
    points = client.scroll(
        collection_name=config.COLLECTION_NAME,
        limit=100,
        with_payload=True,
    )[0]

    # Count by source
    source_counts = {}
    type_counts = {}

    for point in points:
        payload = point.payload or {}
        metadata = payload.get("metadata", {})

        source = metadata.get("source", "unknown")
        doc_type = metadata.get("type", "unknown")

        source_counts[source] = source_counts.get(source, 0) + 1
        type_counts[doc_type] = type_counts.get(doc_type, 0) + 1

    print("\nDocuments by source:")
    for source, count in sorted(source_counts.items()):
        print(f"  - {source}: {count}")

    print("\nDocuments by type:")
    for doc_type, count in sorted(type_counts.items()):
        print(f"  - {doc_type}: {count}")

    # Run sample queries
    if not skip_query:
        print("\n" + "="*60)
        print("TESTING RETRIEVAL QUALITY")
        print("="*60 + "\n")

        # Initialize embeddings and vector store
        embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=config.COLLECTION_NAME,
            embedding=embeddings,
        )

        # Sample queries
        test_queries = [
            "What are James's technical skills?",
            "Tell me about James's work experience",
            "What is James's educational background?",
            "What projects has James worked on?",
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            print("-" * 60)

            results = vector_store.similarity_search_with_score(
                query,
                k=3
            )

            for j, (doc, score) in enumerate(results, 1):
                print(f"\nResult {j} (score: {score:.4f}):")
                print(f"Source: {doc.metadata.get('source', 'unknown')}")
                print(f"Type: {doc.metadata.get('type', 'unknown')}")
                print(f"Content: {doc.page_content[:200]}...")

    print("\n" + "="*60)
    print("VALIDATION COMPLETE!")
    print("="*60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Qdrant ingestion")
    parser.add_argument(
        "--skip-query",
        action="store_true",
        help="Skip running sample queries (saves OpenAI API calls)"
    )

    args = parser.parse_args()
    main(skip_query=args.skip_query)
