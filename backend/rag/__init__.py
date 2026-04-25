# backend/rag/__init__.py
"""
RAG Pipeline — Public API

Usage:
    from rag import retrieve_for_generation, retrieve_for_evaluation
    from rag import ingest_knowledge_base, get_collection_stats

    # On startup:
    ingest_knowledge_base()

    # For quiz generation:
    ctx = retrieve_for_generation("donor retention")
    prompt_context = ctx.to_prompt_string()

    # For answer evaluation:
    ctx = retrieve_for_evaluation("donor retention")
    eval_context = ctx.to_evaluation_string()
"""

from .vector_store import (
    ingest_knowledge_base,
    get_collection,
    get_collection_stats,
)
from .retriever import (
    retrieve_for_generation,
    retrieve_for_evaluation,
    retrieve_email_chunks,
    retrieve_practice_chunks,
    retrieve_question_chunks,
    RAGContext,
    RetrievedChunk,
)

__all__ = [
    # Vector store
    "ingest_knowledge_base",
    "get_collection",
    "get_collection_stats",
    # Retrieval
    "retrieve_for_generation",
    "retrieve_for_evaluation",
    "retrieve_email_chunks",
    "retrieve_practice_chunks",
    "retrieve_question_chunks",
    # Types
    "RAGContext",
    "RetrievedChunk",
]