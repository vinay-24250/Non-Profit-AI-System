# backend/main.py
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
logging.basicConfig(level=logging.INFO)

# ── Validate env on startup ───────────────────────────────────────────────────
_key = os.getenv("GROQ_API_KEY", "")
if not _key or _key == "your_groq_api_key_here":
    raise RuntimeError(
        "\n\n❌  GROQ_API_KEY is not set.\n"
        "    Copy backend/.env.example → backend/.env\n"
        "    Add your key from https://console.groq.com\n"
    )

# Import AFTER env validation
from triage_agent import run_triage_agent                   # noqa: E402
from quiz_engine import generate_question, evaluate_answer  # noqa: E402
from rag import ingest_knowledge_base, get_collection_stats # noqa: E402

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="NonProfit AI Platform",
    description=(
        "Reactive Triage Agent + RAG Quiz Tutor\n"
        "Powered by CrewAI + ChromaDB + Groq Llama 3.3"
    ),
    version="3.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://15.207.184.18:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup: Initialize RAG knowledge base ────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("🚀 NonProfit AI Platform starting up...")
    print("="*60)
    print("\n📚 Initializing RAG knowledge base...")
    summary = ingest_knowledge_base()
    print(f"\n✅ RAG pipeline ready:")
    print(f"   donor_emails   : {summary.get('donor_emails', 0)} embeddings")
    print(f"   best_practices : {summary.get('best_practices', 0)} embeddings")
    print(f"   quiz_bank      : {summary.get('quiz_bank', 0)} embeddings")
    print("\n✅ Backend ready to serve requests\n")


# ── Request models ────────────────────────────────────────────────────────────
class TriageRequest(BaseModel):
    text: str

class QuizGenerateRequest(BaseModel):
    topic:      str
    difficulty: str = "medium"

class QuizEvaluateRequest(BaseModel):
    question:       str
    correct_answer: str
    user_answer:    str
    topic:          str


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status":    "ok",
        "version":   "3.0.0",
        "framework": "crewai",
        "model":     "groq/llama-3.3-70b-versatile",
        "rag":       "enabled",
        "embedding": "all-MiniLM-L6-v2",
    }


# ── RAG stats ─────────────────────────────────────────────────────────────────
@app.get("/api/rag/stats")
def rag_stats():
    """Returns count of embeddings in each ChromaDB collection."""
    try:
        stats = get_collection_stats()
        return {
            "status":      "ok",
            "collections": stats,
            "total":       sum(stats.values()),
            "embed_model": "all-MiniLM-L6-v2",
            "dimensions":  384,
            "distance":    "cosine",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Triage Agent ──────────────────────────────────────────────────────────────
@app.post("/api/triage")
def triage(req: TriageRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="Message text cannot be empty.")
    try:
        return run_triage_agent(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Quiz: Generate ────────────────────────────────────────────────────────────
@app.post("/api/quiz/generate")
def quiz_generate(req: QuizGenerateRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=422, detail="Topic cannot be empty.")
    if req.difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(
            status_code=422,
            detail="Difficulty must be: easy, medium, or hard."
        )
    try:
        return generate_question(req.topic, req.difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Quiz: Evaluate ────────────────────────────────────────────────────────────
@app.post("/api/quiz/evaluate")
def quiz_evaluate(req: QuizEvaluateRequest):
    if not req.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")
    try:
        return evaluate_answer(
            req.question,
            req.correct_answer,
            req.user_answer,
            req.topic,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))