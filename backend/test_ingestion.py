import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "portfolio-chat")


def ensure_db_ready() -> bool:
    path = Path(CHROMA_PERSIST_DIR)
    if not path.exists():
        print(f"❌ Persistence directory not found: {path}")
        return False
    if not any(path.iterdir()):
        print(f"❌ Persistence directory is empty: {path}")
        return False
    return True


def load_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )


def print_collection_stats(vectorstore: Chroma) -> None:
    collection = vectorstore._collection
    total = collection.count()

    def source_count(source: str) -> int:
        try:
            return len(collection.get(where={"source": source})["ids"])
        except Exception:
            return 0

    print("\n=== Chroma Collection Stats ===")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Persisted at: {CHROMA_PERSIST_DIR}")
    print(f"Total vectors: {total}")
    print("By source:")
    for source in ["resume", "portfolio_config", "github", "blog"]:
        count = source_count(source)
        print(f"  - {source}: {count}")


def run_sample_query(vectorstore: Chroma, question: str, k: int) -> None:
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(question)

    print("\n=== Sample Query ===")
    print(f"Question: {question}")
    print(f"Results returned: {len(results)}")
    for idx, doc in enumerate(results, start=1):
        preview = doc.page_content[:160].replace("\n", " ")
        print(f"\nResult {idx}:")
        print(f"  Source: {doc.metadata.get('source', 'unknown')}")
        print(f"  Type: {doc.metadata.get('type', 'unknown')}")
        print(f"  Preview: {preview}...")


def main():
    parser = argparse.ArgumentParser(
        description="Validate the ingested Chroma vector store."
    )
    parser.add_argument(
        "--question",
        default="What are James Brendamour's core skills?",
        help="Sample question to run against the store.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=3,
        help="Number of documents to retrieve for the sample query.",
    )
    parser.add_argument(
        "--skip-query",
        action="store_true",
        help="Skip the sample retrieval step (no OpenAI call).",
    )
    args = parser.parse_args()

    if not ensure_db_ready():
        sys.exit(1)

    try:
        vectorstore = load_vectorstore()
    except Exception as exc:
        print(f"❌ Failed to load vector store: {exc}")
        sys.exit(1)

    print_collection_stats(vectorstore)

    if args.skip-query:
        print("\nSample query skipped by flag.")
        sys.exit(0)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY is not set; skipping sample query.")
        sys.exit(0)

    try:
        run_sample_query(vectorstore, args.question, args.k)
    except Exception as exc:
        print(f"❌ Sample query failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
