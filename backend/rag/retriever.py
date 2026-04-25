# backend/rag/retriever.py
"""
RAG Retrieval Pipeline

This module is the core of the RAG system.
It handles semantic search against ChromaDB and formats
retrieved chunks into structured context for LLM injection.

Retrieval Flow:
  1. Receive query string (topic/scenario from user)
  2. Embed query using same sentence-transformers model as ingestion
  3. ChromaDB runs HNSW approximate nearest neighbor search
  4. Returns top-k chunks ranked by cosine similarity score
  5. Chunks formatted with metadata for LLM prompt injection

Distance metric: cosine similarity
  - Score 0.0 = identical
  - Score 1.0 = completely different
  - We filter out chunks with distance > SIMILARITY_THRESHOLD
"""

import logging
from dataclasses import dataclass
from typing import List
from rag.vector_store import get_collection

logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
SIMILARITY_THRESHOLD = 0.85   # Discard chunks with cosine distance > this value
MIN_CHUNKS           = 1      # Always return at least this many chunks


# ── Data classes for typed retrieval results ──────────────────────────────────
@dataclass
class RetrievedChunk:
    """A single retrieved document chunk with metadata and similarity score."""
    content:  str
    metadata: dict
    distance: float       # cosine distance (lower = more similar)

    @property
    def similarity(self) -> float:
        """Convert cosine distance to similarity score (0-1, higher = better)."""
        return round(1.0 - self.distance, 4)

    def __repr__(self):
        return (
            f"RetrievedChunk(similarity={self.similarity:.3f}, "
            f"topic={self.metadata.get('topic','?')}, "
            f"content={self.content[:60]}...)"
        )


@dataclass
class RAGContext:
    """
    Full context package retrieved for a given topic.
    Contains chunks from all 3 collections ready for LLM injection.
    """
    topic:            str
    email_chunks:     List[RetrievedChunk]
    practice_chunks:  List[RetrievedChunk]
    question_chunks:  List[RetrievedChunk]

    def to_prompt_string(self) -> str:
        """
        Formats all retrieved chunks into a single prompt-ready string.
        This is what gets injected into the LLM prompt.
        """
        parts = []

        if self.email_chunks:
            parts.append("=== RETRIEVED DONOR EMAIL SCENARIOS ===")
            for i, chunk in enumerate(self.email_chunks, 1):
                parts.append(
                    f"\nScenario {i} "
                    f"[category: {chunk.metadata.get('category','?')} | "
                    f"urgency: {chunk.metadata.get('urgency','?')} | "
                    f"similarity: {chunk.similarity:.2f}]:\n"
                    f"{chunk.content}"
                )

        if self.practice_chunks:
            parts.append("\n=== RETRIEVED BEST PRACTICE GUIDELINES ===")
            for i, chunk in enumerate(self.practice_chunks, 1):
                parts.append(
                    f"\nGuideline {i} "
                    f"[topic: {chunk.metadata.get('topic','?')} | "
                    f"similarity: {chunk.similarity:.2f}]:\n"
                    f"{chunk.content}"
                )

        if self.question_chunks:
            parts.append("\n=== RETRIEVED REFERENCE QUESTIONS (style guide only) ===")
            for i, chunk in enumerate(self.question_chunks, 1):
                parts.append(
                    f"\nReference {i} "
                    f"[topic: {chunk.metadata.get('topic','?')} | "
                    f"correct: {chunk.metadata.get('correct_answer','?')} | "
                    f"similarity: {chunk.similarity:.2f}]:\n"
                    f"Q: {chunk.metadata.get('question', chunk.content[:120])}\n"
                    f"Explanation: {chunk.metadata.get('explanation','')}"
                )

        return "\n".join(parts)

    def to_evaluation_string(self) -> str:
        """
        Formats only best practice chunks for evaluation prompt injection.
        Used when evaluating quiz answers — only guidelines are relevant.
        """
        if not self.practice_chunks:
            return "No specific guidelines retrieved for this topic."

        parts = ["=== RETRIEVED BEST PRACTICE GUIDELINES (authoritative reference) ==="]
        for i, chunk in enumerate(self.practice_chunks, 1):
            parts.append(
                f"\nGuideline {i} "
                f"[topic: {chunk.metadata.get('topic','?')} | "
                f"similarity: {chunk.similarity:.2f}]:\n"
                f"{chunk.content}"
            )
        return "\n".join(parts)

    @property
    def total_chunks(self) -> int:
        return len(self.email_chunks) + len(self.practice_chunks) + len(self.question_chunks)


# ── Core retrieval function ───────────────────────────────────────────────────
def _retrieve_chunks(
    collection_name: str,
    query: str,
    n_results: int = 3,
    threshold: float = SIMILARITY_THRESHOLD,
) -> List[RetrievedChunk]:
    """
    Core retrieval function.

    Steps:
      1. Get ChromaDB collection
      2. Embed the query string using sentence-transformers
      3. Run HNSW nearest neighbor search
      4. Filter results by similarity threshold
      5. Return typed RetrievedChunk list sorted by similarity

    Args:
      collection_name : ChromaDB collection to search
      query           : Search string (topic or scenario description)
      n_results       : Max chunks to retrieve before filtering
      threshold       : Max cosine distance to include (lower = stricter)

    Returns:
      List[RetrievedChunk] sorted by similarity (best first)
    """
    try:
        col   = get_collection(collection_name)
        count = col.count()

        if count == 0:
            logger.warning(f"Collection '{collection_name}' is empty.")
            return []

        actual_n = min(n_results, count)
        results  = col.query(
            query_texts=[query],
            n_results=actual_n,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        chunks = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            if dist <= threshold:
                chunks.append(RetrievedChunk(
                    content=doc,
                    metadata=meta or {},
                    distance=float(dist),
                ))

        # Always return at least MIN_CHUNKS even if below threshold
        if not chunks and documents:
            chunks = [
                RetrievedChunk(
                    content=documents[0],
                    metadata=metadatas[0] or {},
                    distance=float(distances[0]),
                )
            ]

        # Sort by similarity (best first)
        chunks.sort(key=lambda c: c.distance)

        logger.info(
            f"[RAG] '{collection_name}' query='{query[:50]}' "
            f"→ {len(chunks)}/{actual_n} chunks passed threshold "
            f"(best similarity: {chunks[0].similarity:.3f})"
        )
        return chunks

    except Exception as e:
        logger.error(f"[RAG] Retrieval error in '{collection_name}': {e}")
        return []


# ── Public retrieval functions ────────────────────────────────────────────────
def retrieve_email_chunks(topic: str, n_results: int = 3) -> List[RetrievedChunk]:
    """
    Retrieve donor email scenarios matching the given topic.
    Used for quiz question generation context.
    """
    return _retrieve_chunks("donor_emails", topic, n_results)


def retrieve_practice_chunks(topic: str, n_results: int = 3) -> List[RetrievedChunk]:
    """
    Retrieve best practice guidelines matching the given topic.
    Used for both question generation and answer evaluation.
    """
    return _retrieve_chunks("best_practices", topic, n_results)


def retrieve_question_chunks(topic: str, n_results: int = 2) -> List[RetrievedChunk]:
    """
    Retrieve reference Q&A pairs for style guidance.
    Used only for question generation — as style reference, not for copying.
    """
    return _retrieve_chunks("quiz_bank", topic, n_results)


def retrieve_for_generation(topic: str) -> RAGContext:
    """
    Full RAG context retrieval for quiz question GENERATION.

    Retrieves from all 3 collections:
      - 3 donor email scenarios (real-world grounding)
      - 3 best practice guidelines (correct answer grounding)
      - 2 reference questions (style and difficulty reference)

    Returns RAGContext with to_prompt_string() method for LLM injection.
    """
    logger.info(f"\n🔍 [RAG Generation] Retrieving context for: '{topic}'")

    ctx = RAGContext(
        topic=topic,
        email_chunks=retrieve_email_chunks(topic, n_results=3),
        practice_chunks=retrieve_practice_chunks(topic, n_results=3),
        question_chunks=retrieve_question_chunks(topic, n_results=2),
    )

    logger.info(
        f"✅ [RAG Generation] Retrieved {ctx.total_chunks} chunks total — "
        f"emails={len(ctx.email_chunks)}, "
        f"practices={len(ctx.practice_chunks)}, "
        f"questions={len(ctx.question_chunks)}"
    )
    return ctx


def retrieve_for_evaluation(topic: str) -> RAGContext:
    """
    RAG context retrieval for quiz answer EVALUATION.

    Retrieves only from best_practices collection —
    the authoritative source for determining if an answer is correct
    and generating grounded explanations.

    Returns RAGContext with to_evaluation_string() method for LLM injection.
    """
    logger.info(f"\n🔍 [RAG Evaluation] Retrieving best practices for: '{topic}'")

    ctx = RAGContext(
        topic=topic,
        email_chunks=[],                                         # not needed for evaluation
        practice_chunks=retrieve_practice_chunks(topic, n_results=3),
        question_chunks=[],                                      # not needed for evaluation
    )

    logger.info(
        f"✅ [RAG Evaluation] Retrieved {len(ctx.practice_chunks)} "
        f"best practice chunks"
    )
    return ctx


# ── Legacy compatibility wrappers ─────────────────────────────────────────────
# Keep these so nothing else breaks if called with old signatures

def retrieve_quiz_context(topic: str) -> dict:
    """Legacy wrapper — returns dict for backward compatibility."""
    ctx = retrieve_for_generation(topic)
    return {
        "similar_emails":    ctx.to_prompt_string(),
        "best_practices":    ctx.to_evaluation_string(),
        "similar_questions": ctx.to_prompt_string(),
        "rag_context":       ctx,
    }


def retrieve_best_practices(topic: str, n_results: int = 2) -> str:
    """Legacy wrapper — returns formatted string for backward compatibility."""
    chunks = retrieve_practice_chunks(topic, n_results)
    if not chunks:
        return "No best practices found."
    return "\n\n".join(
        f"Guideline [topic: {c.metadata.get('topic','?')} | similarity: {c.similarity:.2f}]:\n{c.content}"
        for c in chunks
    )