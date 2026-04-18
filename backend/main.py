# backend/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

# ── Validate environment on startup ──────────────────────────────────────────
_key = os.getenv("GROQ_API_KEY", "")
if not _key or _key == "your_groq_api_key_here":
    raise RuntimeError(
        "\n\n❌  GROQ_API_KEY is not set.\n"
        "    1. Copy backend/.env.example  →  backend/.env\n"
        "    2. Add your key from https://console.groq.com\n"
    )

# Import crews AFTER env validation so they don't fail silently
from triage_agent import run_triage_agent        # noqa: E402
from quiz_engine import generate_question, evaluate_answer  # noqa: E402

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="NonProfit AI Platform",
    description="Triage Agent + Quiz Bot — powered by CrewAI + Llama 3.1 via Groq",
    version="2.0.0",
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


# ── Pydantic Models ───────────────────────────────────────────────────────────
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
        "status": "ok",
        "framework": "crewai==0.51.0",
        "model": "llama-3.3-70b-versatile",
    }


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
            detail="Difficulty must be one of: easy, medium, hard."
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