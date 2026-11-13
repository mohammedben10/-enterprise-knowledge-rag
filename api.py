"""
Enterprise Knowledge RAG — FastAPI Service
------------------------------------------
Production-ready REST API allowing external portals, Slackbots, or web apps
to query Apex Global corporate knowledge and policy guidelines.
"""

from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
from rag_engine import EnterpriseRAGEngine
from load_docs import load_markdown_documents

app = FastAPI(
    title="Apex Global — Enterprise Knowledge Copilot API",
    description="REST API for querying company policies, HR benefits, IT security, and customer SLAs.",
    version="1.0.0"
)

# Enable CORS for internal frontend portals or dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy singleton engine instance
_engine: Optional[EnterpriseRAGEngine] = None


def get_engine() -> EnterpriseRAGEngine:
    global _engine
    if _engine is None:
        _engine = EnterpriseRAGEngine()
    return _engine


# Pydantic schemas
class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message text")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, description="The policy or business question")
    chat_history: Optional[List[ChatMessage]] = Field(default=[], description="Previous conversation turns")


class SourceItem(BaseModel):
    file: str
    title: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
    retrieved_chunks_count: int


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Apex Global Enterprise Knowledge Copilot",
        "status": "online",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "model": config.GEMINI_MODEL,
        "embedding_model": config.EMBEDDING_MODEL_NAME,
        "collection": config.COLLECTION_NAME
    }


@app.get("/documents", tags=["Knowledge Base"])
def list_documents():
    """List all official policy documents currently loaded into the system."""
    docs = load_markdown_documents(config.DOCS_DIR)
    return {
        "total_documents": len(docs),
        "documents": [
            {
                "file": d["source"],
                "title": d["title"],
                "length_characters": len(d["content"])
            }
            for d in docs
        ]
    }


@app.post("/ask", response_model=AskResponse, tags=["RAG Query"])
def ask_question(request: AskRequest):
    """Ask a question against official enterprise policy documentation."""
    try:
        engine = get_engine()
        # Convert Pydantic objects to dicts
        history = [msg.model_dump() for msg in request.chat_history] if request.chat_history else None
        result = engine.query(question=request.question, chat_history=history)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
