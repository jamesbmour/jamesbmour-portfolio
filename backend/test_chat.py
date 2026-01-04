"""
Test script for the chat API endpoint.
Sends sample questions and validates responses.
"""
import asyncio
import requests
from typing import List, Dict


BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("="*60)
    print("Testing Health Check")
    print("="*60 + "\n")

    try:
        response = requests.get(f"{BASE_URL}/api/health")
        response.raise_for_status()

        data = response.json()
        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        print(f"Vector Store: {data.get('vector_store')}")

        if 'collection' in data:
            print(f"Collection: {data.get('collection')}")
            print(f"Vector Count: {data.get('vector_count')}")

        return data.get('status') == 'healthy'

    except Exception as e:
        print(f"✗ Health check failed: {str(e)}")
        return False


def test_chat_query(message: str):
    """
    Test a single chat query.

    Args:
        message: User's question
    """
    print(f"\nQuery: {message}")
    print("-" * 60)

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            print(f"\nResponse: {data.get('response')}")

            sources = data.get('sources', [])
            if sources:
                print(f"\nSources ({len(sources)}):")
                for i, source in enumerate(sources, 1):
                    metadata = source.get('metadata', {})
                    print(f"\n  {i}. Type: {metadata.get('type', 'unknown')}")
                    print(f"     Source: {metadata.get('source', 'unknown')}")
                    print(f"     Content: {source.get('content', '')[:100]}...")
        else:
            print(f"✗ Query failed: {data.get('error', 'Unknown error')}")

        return data.get('success', False)

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CHAT API TESTING")
    print("="*60 + "\n")

    # Check if server is running
    print("Checking if backend server is running...")
    try:
        requests.get(BASE_URL, timeout=2)
        print("✓ Server is running\n")
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running!")
        print("Start the server with: uvicorn main:app --reload")
        return
    except Exception as e:
        print(f"✗ Error connecting to server: {str(e)}")
        return

    # Test health check
    healthy = test_health_check()

    if not healthy:
        print("\n✗ Health check failed. Cannot proceed with chat tests.")
        print("Make sure you have run 'python ingest.py' first.")
        return

    print("\n" + "="*60)
    print("Testing Chat Queries")
    print("="*60)

    # Test queries
    test_queries = [
        "What programming languages does James know?",
        "Tell me about James's experience at EY",
        "What is James's educational background?",
        "What projects has James worked on?",
        "What blog articles has James written?",
        "What certifications does James have?",
    ]

    successful = 0
    failed = 0

    for query in test_queries:
        success = test_chat_query(query)
        if success:
            successful += 1
        else:
            failed += 1

        print("\n" + "-"*60)

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"\nTotal Queries: {len(test_queries)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {failed} test(s) failed")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
