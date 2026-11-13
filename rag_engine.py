"""
Enterprise RAG Engine
---------------------
Orchestrates semantic document retrieval and generative question-answering
using ChromaDB vector search and the official Google GenAI SDK.
"""

import os
import time
from typing import List, Dict, Any, Optional

# Disable ChromaDB telemetry
os.environ["ANONYMOUS_TELEMETRY"] = "False"

from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

import config


class EnterpriseRAGEngine:
    """
    RAG Assistant for enterprise business policies, operations,
    HR guidelines, corporate travel, procurement limits, IT security, and SLAs.
    """

    def __init__(self, top_k: int = config.DEFAULT_TOP_K, model_name: Optional[str] = None):
        self.top_k = top_k
        self.model_name = model_name or config.GEMINI_MODEL

        # Validate Gemini API key
        if not config.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is missing. Please set it in your .env file or environment."
            )

        print(f"🔧 Initializing Enterprise RAG Engine with model: {self.model_name}...")

        # 1. Initialize Google Gemini Embeddings for retrieval
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=config.GOOGLE_API_KEY
        )

        # 2. Connect to persistent ChromaDB collection
        self.vector_db = Chroma(
            collection_name=config.COLLECTION_NAME,
            persist_directory=str(config.CHROMA_DIR),
            embedding_function=self.embeddings
        )

        # 3. Initialize official Google GenAI client
        self.ai_client = genai.Client(api_key=config.GOOGLE_API_KEY)

        print("✨ Enterprise RAG Engine is ready!")

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Any]:
        """Retrieve the top matching document chunks from the vector store."""
        k = top_k or self.top_k
        return self.vector_db.similarity_search(query, k=k)

    def query(self, question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        End-to-end RAG query:
        1. Retrieve relevant company policy chunks.
        2. Format multi-turn conversation context.
        3. Call Gemini to generate a verified, sourced response.
        """
        # 1. Retrieve relevant policy sections
        retrieved_docs = self.retrieve(question)

        # 2. Extract and format context
        context_parts = []
        sources = []
        seen_sources = set()

        for doc in retrieved_docs:
            source_file = doc.metadata.get("source", "Unknown Document")
            title = doc.metadata.get("title", source_file)
            chunk_content = doc.page_content.strip()

            context_parts.append(f"--- Document: {title} ({source_file}) ---\n{chunk_content}")

            if source_file not in seen_sources:
                sources.append({
                    "file": source_file,
                    "title": title
                })
                seen_sources.add(source_file)

        formatted_context = "\n\n".join(context_parts)

        # 3. Format previous conversation turns if provided
        history_text = ""
        if chat_history:
            history_lines = []
            for item in chat_history[-4:]:  # Keep recent turns for concise memory
                role = item.get("role", "user").capitalize()
                content = item.get("content", "")
                history_lines.append(f"{role}: {content}")
            history_text = "\n".join(history_lines)

        # 4. Construct instructions
        system_instructions = (
            "You are the official Enterprise AI Knowledge Assistant for Apex Global Technologies.\n"
            "Your role is to assist employees, managers, and executives by answering questions about "
            "company operations, HR benefits, corporate travel, procurement thresholds, IT security, "
            "customer support SLAs, and commercial pricing.\n\n"
            "STRICT GUIDELINES:\n"
            "1. Ground your answer ONLY in the COMPANY CONTEXT provided below. Do not guess or hallucinate.\n"
            "2. If an exact answer is not present in the context, explicitly state: "
            "'This information is not covered in our current policy documents. Please contact the appropriate department (e.g., #ask-hr, #ask-finance, or #it-helpdesk).' \n"
            "3. Be concise, professional, and clear. Use structured bullet points when listing steps, figures, or tiers.\n"
            "4. Always mention the relevant policy document or section when stating guidelines.\n"
        )

        user_prompt = f"""
{system_instructions}

==================== COMPANY CONTEXT ====================
{formatted_context}
=========================================================

{f"CONVERSATION HISTORY:\n{history_text}\n" if history_text else ""}
QUESTION: {question}

OFFICIAL POLICY ANSWER:
""".strip()

        # 5. Invoke Google Gemini with resilient retry
        answer_text = "No response generated."
        for attempt in range(2):
            try:
                response = self.ai_client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt
                )
                answer_text = response.text.strip() if response.text else "No response generated."
                break
            except Exception as e:
                if attempt == 1:
                    raise
                time.sleep(1.5)

        return {
            "question": question,
            "answer": answer_text,
            "sources": sources,
            "retrieved_chunks_count": len(retrieved_docs)
        }
