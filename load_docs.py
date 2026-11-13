"""
Document Ingestion Pipeline
---------------------------
Reads corporate markdown policy documents, splits them into logical chunks,
computes semantic embeddings using Google Gemini Embeddings, and stores
them into a persistent ChromaDB vector store.
"""

import os
from pathlib import Path

# Disable ChromaDB anonymous telemetry
os.environ["ANONYMOUS_TELEMETRY"] = "False"

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

import config


def load_markdown_documents(docs_folder: Path):
    """Scan docs directory and load all markdown files with metadata."""
    if not docs_folder.exists():
        raise FileNotFoundError(f"Documents folder not found: {docs_folder}")

    loaded_docs = []
    md_files = list(docs_folder.glob("*.md"))

    if not md_files:
        print(f"⚠️ No markdown files found in {docs_folder}")
        return loaded_docs

    print(f"📂 Found {len(md_files)} business policy documents in '{docs_folder.name}':")
    for file_path in sorted(md_files):
        content = file_path.read_text(encoding="utf-8").strip()
        # Extract title from the first heading if available
        first_line = content.splitlines()[0] if content else file_path.stem
        title = first_line.lstrip("#").strip() if first_line.startswith("#") else file_path.stem

        print(f"   • {file_path.name}  ->  '{title}'")
        loaded_docs.append({
            "source": file_path.name,
            "title": title,
            "content": content
        })

    return loaded_docs


def split_into_chunks(documents):
    """
    Split long policy documents into smaller, overlapping chunks
    so the retrieval engine can find precise sections.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )

    chunks = []
    metadatas = []

    for doc in documents:
        splits = text_splitter.split_text(doc["content"])
        for idx, chunk_text in enumerate(splits):
            chunks.append(chunk_text)
            metadatas.append({
                "source": doc["source"],
                "title": doc["title"],
                "chunk_id": idx,
                "total_chunks": len(splits)
            })

    return chunks, metadatas


def get_embeddings():
    """Initialize Google Gemini Embeddings."""
    if not config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

    return GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GOOGLE_API_KEY
    )


def build_vector_database():
    """
    Ingest all business documents, generate vector embeddings, and save to ChromaDB.
    """
    print("\n" + "=" * 60)
    print("🚀 Ingesting Enterprise Knowledge Base into ChromaDB")
    print("=" * 60)

    # 1. Load markdown files
    documents = load_markdown_documents(config.DOCS_DIR)
    if not documents:
        print("❌ Ingestion stopped: No documents to process.")
        return None

    # 2. Chunk documents
    chunks, metadatas = split_into_chunks(documents)
    print(f"\n🧩 Split {len(documents)} documents into {len(chunks)} contextual chunks.")

    # 3. Load embeddings
    print(f"🧠 Connecting to embedding model: '{config.EMBEDDING_MODEL}'...")
    embeddings = get_embeddings()

    # 4. Store in ChromaDB
    print("💾 Generating embeddings and storing vectors into ChromaDB...")
    db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.CHROMA_DIR)
    )

    print("✅ Vector database successfully built and persisted to disk!")
    print(f"   Stored at: {config.CHROMA_DIR}")
    print(f"   Collection: {config.COLLECTION_NAME}")
    print("=" * 60 + "\n")
    return db


if __name__ == "__main__":
    build_vector_database()
