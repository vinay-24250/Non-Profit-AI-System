# backend/quiz_engine.py
"""
RAG-Driven Quiz Engine

Pipeline for Question Generation:
  1. User selects topic/scenario
  2. retrieve_for_generation(topic) → queries ChromaDB
     - Embeds topic string → 384-dim vector
     - Cosine similarity search across 3 collections
     - Returns top-k chunks: emails + best_practices + reference_questions
  3. ctx.to_prompt_string() → formats all chunks into prompt context
  4. CrewAI agent receives context → Groq LLM generates grounded MCQ
  5. Response includes rag_grounded=True and chunk count

Pipeline for Answer Evaluation:
  1. User submits answer
  2. Correctness determined locally (no LLM hallucination risk)
  3. retrieve_for_evaluation(topic) → queries only best_practices collection
  4. ctx.to_evaluation_string() → formats guidelines into evaluator prompt
  5. CrewAI agent receives guidelines → Groq LLM generates grounded explanation
"""

import os
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from rag import retrieve_for_generation, retrieve_for_evaluation
from tools.json_parser_tool import parse_json_output

load_dotenv()
logger = logging.getLogger(__name__)


# ── LLM factory ───────────────────────────────────────────────────────────────
def get_llm(temperature: float = 0.5) -> LLM:
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
    )


# ── Safe output extractor ─────────────────────────────────────────────────────
def _extract_output(result, index: int = 0) -> str:
    """Safely extract raw task output across crewai versions."""
    try:
        outputs = result.tasks_output
        if outputs and len(outputs) > index:
            raw = outputs[index].raw
            if raw:
                return raw
    except AttributeError:
        pass
    try:
        return result.raw
    except AttributeError:
        return str(result)


# ══════════════════════════════════════════════════════════════════════════════
# QUESTION GENERATION — RAG Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def generate_question(topic: str, difficulty: str = "medium") -> dict:
    """
    Generate a grounded MCQ question using the RAG pipeline.

    RAG Steps:
      1. Embed topic → search donor_emails, best_practices, quiz_bank
      2. Retrieve top-k semantically similar chunks
      3. Format chunks into structured prompt context
      4. LLM generates question BASED ON retrieved real examples
         — not from imagination
    """
    # ── Step 1: RAG Retrieval ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"🔍 RAG PIPELINE — Question Generation")
    print(f"   Topic     : {topic}")
    print(f"   Difficulty: {difficulty}")
    print(f"{'='*60}")

    ctx = retrieve_for_generation(topic)

    print(f"\n📦 Retrieved chunks:")
    print(f"   Email scenarios   : {len(ctx.email_chunks)} chunks")
    print(f"   Best practices    : {len(ctx.practice_chunks)} chunks")
    print(f"   Reference Q&As    : {len(ctx.question_chunks)} chunks")
    print(f"   Total             : {ctx.total_chunks} chunks")

    if ctx.email_chunks:
        print(f"\n   Top email similarity   : {ctx.email_chunks[0].similarity:.3f}")
    if ctx.practice_chunks:
        print(f"   Top practice similarity: {ctx.practice_chunks[0].similarity:.3f}")

    # ── Step 2: Format context for LLM injection ──────────────────────────────
    rag_context_str = ctx.to_prompt_string()
    print(f"\n✅ Context formatted — injecting {len(rag_context_str)} chars into prompt")

    # ── Step 3: Difficulty guidance ───────────────────────────────────────────
    difficulty_hints = {
        "easy":   "a straightforward factual question — one option is clearly right",
        "medium": "a scenario-based question requiring practical judgement",
        "hard":   "a complex multi-factor question requiring deep understanding",
    }
    difficulty_hint = difficulty_hints.get(difficulty, "a scenario-based question")

    # ── Step 4: CrewAI Agent ──────────────────────────────────────────────────
    llm = get_llm(temperature=0.7)

    agent = Agent(
        role="Non-Profit Training Expert",
        goal=(
            "Create accurate, grounded multiple-choice quiz questions "
            "strictly based on the retrieved real donor email scenarios "
            "and established best practice guidelines. "
            "Never invent scenarios — every question must be grounded "
            "in the provided context."
        ),
        backstory=(
            "You are a senior trainer at a Non-Profit learning institute "
            "with 15 years of experience. You have access to a curated "
            "knowledge base of real donor emails and verified best practice "
            "guidelines retrieved from ChromaDB. You use this context "
            "exclusively to create realistic, accurate, and educational "
            "assessment questions."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # ── Step 5: Task with RAG context injected ────────────────────────────────
    task_description = (
        "Create a multiple-choice quiz question using ONLY the retrieved context below.\n\n"
        "Topic     : " + topic + "\n"
        "Difficulty: " + difficulty + " — " + difficulty_hint + "\n\n"
        + rag_context_str + "\n\n"
        "=== INSTRUCTIONS ===\n"
        "- Base your question on REAL scenarios from the retrieved email examples above\n"
        "- The correct answer MUST align with the retrieved best practice guidelines\n"
        "- Create a NEW original question — do NOT copy reference questions\n"
        "- All 4 options must be plausible NonProfit scenarios — no obviously wrong answers\n"
        "- The question must test practical knowledge a NonProfit staff member needs\n\n"
        "Return ONLY this exact JSON structure:\n"
        "{\n"
        '  "question": "Full scenario-based question text here?",\n'
        '  "options": [\n'
        '    "A. First option",\n'
        '    "B. Second option",\n'
        '    "C. Third option",\n'
        '    "D. Fourth option"\n'
        '  ],\n'
        '  "correct_answer": "A",\n'
        '  "topic": "' + topic + '",\n'
        '  "difficulty": "' + difficulty + '"\n'
        "}\n\n"
        "CRITICAL: Return ONLY the JSON object. No markdown. No backticks. No explanation."
    )

    task = Task(
        description=task_description,
        expected_output=(
            "A valid JSON object with keys: question, options (array of 4), "
            "correct_answer (single letter A/B/C/D), topic, difficulty."
        ),
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    # ── Step 6: Run and parse ─────────────────────────────────────────────────
    result = crew.kickoff()
    raw    = _extract_output(result, 0)
    parsed = parse_json_output(raw)

    # Attach RAG metadata
    parsed["rag_grounded"]   = True
    parsed["chunks_used"]    = ctx.total_chunks
    parsed["top_similarity"] = (
        ctx.email_chunks[0].similarity if ctx.email_chunks
        else ctx.practice_chunks[0].similarity if ctx.practice_chunks
        else 0.0
    )

    print(f"\n✅ Question generated — rag_grounded=True, chunks_used={ctx.total_chunks}")
    return parsed


# ══════════════════════════════════════════════════════════════════════════════
# ANSWER EVALUATION — RAG Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def evaluate_answer(
    question:       str,
    correct_answer: str,
    user_answer:    str,
    topic:          str,
) -> dict:
    """
    Evaluate a quiz answer using the RAG pipeline.

    RAG Steps:
      1. Determine correctness LOCALLY — never trust LLM for binary check
      2. Embed topic → search best_practices collection only
      3. Retrieve top-k guideline chunks
      4. Format guidelines into evaluator prompt
      5. LLM generates explanation GROUNDED in retrieved guidelines
    """
    # ── Step 1: Local correctness check (no LLM) ─────────────────────────────
    is_correct   = user_answer.strip().upper() == correct_answer.strip().upper()
    result_label = "CORRECT" if is_correct else "INCORRECT"

    print(f"\n{'='*60}")
    print(f"🔍 RAG PIPELINE — Answer Evaluation")
    print(f"   Topic      : {topic}")
    print(f"   User answer: {user_answer} | Correct: {correct_answer}")
    print(f"   Result     : {result_label}")
    print(f"{'='*60}")

    # ── Step 2: RAG Retrieval — best practices only ───────────────────────────
    ctx = retrieve_for_evaluation(topic)

    print(f"\n📦 Retrieved chunks:")
    print(f"   Best practice chunks: {len(ctx.practice_chunks)}")
    if ctx.practice_chunks:
        print(f"   Top similarity      : {ctx.practice_chunks[0].similarity:.3f}")

    # ── Step 3: Format evaluation context ────────────────────────────────────
    eval_context_str = ctx.to_evaluation_string()
    print(f"\n✅ Evaluation context formatted — "
          f"injecting {len(eval_context_str)} chars into prompt")

    # ── Step 4: CrewAI Evaluator Agent ───────────────────────────────────────
    llm = get_llm(temperature=0.2)

    agent = Agent(
        role="Learning Assessment Specialist",
        goal=(
            "Evaluate quiz answers using the retrieved NonProfit best practice "
            "guidelines as the ONLY authoritative reference. "
            "Explanations must cite specific guidelines from the retrieved context. "
            "Never give generic advice — every explanation must be grounded."
        ),
        backstory=(
            "You are a NonProfit communications educator with access to a "
            "verified knowledge base of best practice guidelines retrieved "
            "from ChromaDB. You use these guidelines as the authoritative source "
            "to explain why answers are correct or incorrect, making learning "
            "specific, actionable, and grounded in real organizational policy."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # ── Step 5: Task with RAG guidelines injected ─────────────────────────────
    task_description = (
        "Evaluate this quiz answer using the retrieved best practice guidelines below.\n\n"
        "Question      : " + question + "\n"
        "Correct Answer: " + correct_answer + "\n"
        "Student Answer: " + user_answer + "\n"
        "Topic         : " + topic + "\n"
        "Result        : " + result_label + "\n\n"
        + eval_context_str + "\n\n"
        "=== INSTRUCTIONS ===\n"
        "- Your explanation MUST reference specific guidelines from the context above\n"
        "- Quote specific protocols, timelines, or rules from the retrieved guidelines\n"
        "- The real_world_example must be a concrete NonProfit scenario from the context\n"
        "- Do NOT give generic advice — every sentence must be grounded in the guidelines\n"
        "- is_correct is already determined: " + result_label + "\n\n"
        "Return ONLY this exact JSON structure:\n"
        "{\n"
        '  "is_correct": ' + str(is_correct).lower() + ",\n"
        '  "score": <integer 0 to 100>,\n'
        '  "feedback": "One specific sentence referencing the retrieved guideline",\n'
        '  "explanation": "2-3 sentences citing specific protocols from the guidelines above",\n'
        '  "real_world_example": "A concrete NonProfit scenario grounded in the context",\n'
        '  "next_difficulty": "easy" or "medium" or "hard"\n'
        "}\n\n"
        "Rules:\n"
        "- score: 85-100 if correct, 0-40 if wrong\n"
        "- next_difficulty: increase one level if correct, decrease one level if wrong\n"
        "CRITICAL: Return ONLY the JSON. No markdown. No backticks. No explanation."
    )

    task = Task(
        description=task_description,
        expected_output=(
            "A valid JSON with: is_correct, score, feedback, "
            "explanation, real_world_example, next_difficulty."
        ),
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    # ── Step 6: Run and parse ─────────────────────────────────────────────────
    result = crew.kickoff()
    raw    = _extract_output(result, 0)
    parsed = parse_json_output(raw)

    # Enforce our own correctness — never override with LLM value
    parsed["is_correct"]      = is_correct
    parsed["rag_grounded"]    = True
    parsed["chunks_used"]     = len(ctx.practice_chunks)

    print(f"\n✅ Evaluation complete — rag_grounded=True, "
          f"is_correct={is_correct}, score={parsed.get('score','?')}")
    return parsed