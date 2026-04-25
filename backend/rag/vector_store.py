# backend/rag/vector_store.py
"""
ChromaDB Vector Store — Embedding Pipeline

Flow:
  1. Documents loaded from knowledge_base.py
  2. sentence-transformers (all-MiniLM-L6-v2) converts each doc to 384-dim vector
  3. Vectors + metadata stored in ChromaDB PersistentClient (persists to disk)
  4. At query time: query string → embed → cosine similarity → top-k chunks returned

Collections:
  - donor_emails    : 15 email scenarios  (384-dim embeddings)
  - best_practices  : 12 guidelines       (384-dim embeddings)
  - quiz_bank       : 8 Q&A reference     (384-dim embeddings)
"""

import os
import logging
import chromadb
from chromadb.utils import embedding_functions
from rag.knowledge_base import DONOR_EMAILS, BEST_PRACTICES, QUIZ_QA_BANK

logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
DB_PATH    = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
EMBED_MODEL = "all-MiniLM-L6-v2"   # 384-dim, fast, accurate for semantic search

# ── Singletons ────────────────────────────────────────────────────────────────
_client: chromadb.PersistentClient = None
_embed_fn = None
_collections: dict = {}


# ── Client ────────────────────────────────────────────────────────────────────
def get_client() -> chromadb.PersistentClient:
    """
    Returns singleton ChromaDB PersistentClient.
    Data persists to disk at backend/chroma_db/
    """
    global _client
    if _client is None:
        os.makedirs(DB_PATH, exist_ok=True)
        _client = chromadb.PersistentClient(path=DB_PATH)
        logger.info(f"ChromaDB client initialized at: {DB_PATH}")
    return _client


# ── Embedding Function ────────────────────────────────────────────────────────
def get_embedding_fn():
    """
    Returns singleton sentence-transformers embedding function.
    Model: all-MiniLM-L6-v2
    - Output: 384-dimensional dense vectors
    - Downloaded automatically on first use (~22MB)
    - Runs locally — no API key needed
    - Distance metric: cosine similarity
    """
    global _embed_fn
    if _embed_fn is None:
        logger.info(f"Loading embedding model: {EMBED_MODEL}")
        _embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL
        )
        logger.info("Embedding model loaded.")
    return _embed_fn


# ── Collection accessor ───────────────────────────────────────────────────────
def get_collection(name: str) -> chromadb.Collection:
    """
    Get or create a ChromaDB collection with cosine similarity distance.
    Collections are cached in memory after first access.
    """
    global _collections
    if name not in _collections:
        client   = get_client()
        embed_fn = get_embedding_fn()
        _collections[name] = client.get_or_create_collection(
            name=name,
            embedding_function=embed_fn,
            metadata={"hnsw:space": "cosine"},   # cosine similarity for semantic matching
        )
        logger.info(
            f"Collection '{name}' ready — "
            f"{_collections[name].count()} documents"
        )
    return _collections[name]


# ── Ingestion ─────────────────────────────────────────────────────────────────
def ingest_knowledge_base(force: bool = False) -> dict:
    """
    Embed and store all knowledge base documents into ChromaDB.

    Process for each document:
      1. Text content extracted from knowledge_base.py
      2. sentence-transformers converts text → 384-dim vector
      3. Vector + metadata stored in ChromaDB collection
      4. ChromaDB builds HNSW index for fast approximate nearest neighbor search

    Skips collections that already have data (unless force=True).
    Returns a summary dict of what was ingested.
    """
    summary = {}

    # ── 1. Donor Emails ───────────────────────────────────────────────────────
    emails_col = get_collection("donor_emails")
    if emails_col.count() == 0 or force:
        print("\n📥 Embedding donor emails → ChromaDB...")
        emails_col.upsert(
            ids=[e["id"] for e in DONOR_EMAILS],
            documents=[e["content"] for e in DONOR_EMAILS],
            metadatas=[
                {
                    "topic":    e["topic"],
                    "category": e["category"],
                    "urgency":  e["urgency"],
                    "scenario": e["scenario"],
                }
                for e in DONOR_EMAILS
            ],
        )
        count = emails_col.count()
        summary["donor_emails"] = count
        print(f"   ✅ {count} donor email embeddings stored")
    else:
        summary["donor_emails"] = emails_col.count()
        print(f"   ✅ donor_emails: {emails_col.count()} embeddings already exist")

    # ── 2. Best Practices ─────────────────────────────────────────────────────
    bp_col = get_collection("best_practices")
    if bp_col.count() == 0 or force:
        print("📥 Embedding best practice guidelines → ChromaDB...")
        bp_col.upsert(
            ids=[b["id"] for b in BEST_PRACTICES],
            documents=[b["content"] for b in BEST_PRACTICES],
            metadatas=[{"topic": b["topic"]} for b in BEST_PRACTICES],
        )
        count = bp_col.count()
        summary["best_practices"] = count
        print(f"   ✅ {count} best practice embeddings stored")
    else:
        summary["best_practices"] = bp_col.count()
        print(f"   ✅ best_practices: {bp_col.count()} embeddings already exist")

    # ── 3. Quiz Q&A Bank ──────────────────────────────────────────────────────
    quiz_col = get_collection("quiz_bank")
    if quiz_col.count() == 0 or force:
        print("📥 Embedding quiz Q&A bank → ChromaDB...")
        quiz_col.upsert(
            ids=[q["id"] for q in QUIZ_QA_BANK],
            # Embed question + all options together for better semantic matching
            documents=[
                q["question"] + " " + " ".join(q["options"])
                for q in QUIZ_QA_BANK
            ],
            metadatas=[
                {
                    "topic":          q["topic"],
                    "correct_answer": q["correct_answer"],
                    "explanation":    q["explanation"],
                    "question":       q["question"],
                }
                for q in QUIZ_QA_BANK
            ],
        )
        count = quiz_col.count()
        summary["quiz_bank"] = count
        print(f"   ✅ {count} quiz Q&A embeddings stored")
    else:
        summary["quiz_bank"] = quiz_col.count()
        print(f"   ✅ quiz_bank: {quiz_col.count()} embeddings already exist")

    total = sum(summary.values())
    print(f"\n✅ ChromaDB ready — {total} total embeddings across 3 collections\n")
    return summary


# ── Collection stats ──────────────────────────────────────────────────────────
def get_collection_stats() -> dict:
    """Returns count of documents in each collection."""
    return {
        "donor_emails":   get_collection("donor_emails").count(),
        "best_practices": get_collection("best_practices").count(),
        "quiz_bank":      get_collection("quiz_bank").count(),
    }