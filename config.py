import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base project paths
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Google Gemini API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
# Default to gemini-3.5-flash (fast, highly capable, and fully active)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# High-fidelity semantic embedding model from Google
# (Fast, accurate 3072-dimension vectors with zero local PyTorch latency)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

# Document chunking parameters
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval settings
DEFAULT_TOP_K = 3
COLLECTION_NAME = "apex_enterprise_policies"
