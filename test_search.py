"""
Quick Similarity Search Verification
------------------------------------
Tests direct semantic retrieval against the ChromaDB vector database.
"""

import os
os.environ["ANONYMOUS_TELEMETRY"] = "False"

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import config


def test_quick_search():
    print(f"Connecting to embedding model '{config.EMBEDDING_MODEL}'...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GOOGLE_API_KEY
    )

    print(f"Connecting to ChromaDB collection '{config.COLLECTION_NAME}'...")
    db = Chroma(
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.CHROMA_DIR),
        embedding_function=embeddings
    )

    query = "What is the policy for booking flights over 6 hours?"
    print(f"\n🔎 Query: '{query}'")
    results = db.similarity_search(query, k=2)

    for i, doc in enumerate(results, start=1):
        print(f"\n--- Result #{i} from: {doc.metadata.get('source')} ---")
        print(doc.page_content[:300] + "...\n")


if __name__ == "__main__":
    test_quick_search()
