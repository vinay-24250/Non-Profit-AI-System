# backend/quiz_engine.py
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools.json_parser_tool import parse_json_output

load_dotenv()


# ── LLM Setup ────────────────────────────────────────────────────────────────
def get_llm(temperature: float = 0.5):
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
    )


# ── Safe Output Extraction ───────────────────────────────────────────────────
def _extract_task_output(result, index: int = 0) -> str:
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


# ── Generate Question ─────────────────────────────────────────────────────────
def generate_question(topic: str, difficulty: str = "medium") -> dict:
    llm = get_llm(temperature=0.8)

    agent = Agent(
        role="Non-Profit Training Expert",
        goal="Create high-quality multiple-choice quiz questions.",
        backstory="You are a senior trainer creating realistic assessments.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    description = f"""
Create a multiple-choice quiz question.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY VALID JSON.

STRICT RULES:
- Use double quotes for ALL keys and values
- Do NOT repeat keys
- No extra text

Format:
{{
  "question": "Full question?",
  "options": ["A. option", "B. option", "C. option", "D. option"],
  "correct_answer": "A",
  "topic": "{topic}",
  "difficulty": "{difficulty}"
}}
"""

    task = Task(
        description=description,
        expected_output="Valid JSON with question, options, correct_answer, topic, difficulty",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    try:
        return parse_json_output(_extract_task_output(result, 0))
    except Exception as e:
        print("GENERATION JSON ERROR:", e)

        # Fallback (prevents 500 error)
        return {
            "question": "Fallback question: What is Java?",
            "options": [
                "A. Programming language",
                "B. Coffee",
                "C. OS",
                "D. Browser"
            ],
            "correct_answer": "A",
            "topic": topic,
            "difficulty": difficulty
        }


# ── Evaluate Answer ───────────────────────────────────────────────────────────
def evaluate_answer(question, correct_answer, user_answer, topic):
    llm = get_llm(temperature=0.3)

    # Determine correctness (never trust LLM for this)
    is_correct = user_answer.strip().upper() == correct_answer.strip().upper()
    result_label = "CORRECT" if is_correct else "INCORRECT"

    agent = Agent(
        role="Learning Assessment Specialist",
        goal="Evaluate answers and give feedback.",
        backstory="You are an expert educator.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    description = f"""
Evaluate this quiz answer.

Question: {question}
Correct Answer: {correct_answer}
Student Answer: {user_answer}
Result: {result_label}

Return ONLY VALID JSON.

STRICT RULES:
- Use double quotes everywhere
- Do NOT repeat keys
- No extra text

Format:
{{
  "is_correct": {str(is_correct).lower()},
  "score": 90,
  "feedback": "Short feedback",
  "explanation": "2-3 sentences",
  "real_world_example": "One example",
  "next_difficulty": "medium"
}}
"""

    task = Task(
        description=description,
        expected_output="Valid JSON with is_correct, score, feedback, explanation, real_world_example, next_difficulty",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    try:
        parsed = parse_json_output(_extract_task_output(result, 0))
    except Exception as e:
        print("EVALUATION JSON ERROR:", e)

        # Fallback (prevents crash)
        parsed = {
            "is_correct": is_correct,
            "score": 50,
            "feedback": "AI response formatting failed.",
            "explanation": "The model returned invalid JSON, so fallback was used.",
            "real_world_example": "AI systems sometimes produce malformed output.",
            "next_difficulty": "medium"
        }

    # Always enforce correctness
    parsed["is_correct"] = is_correct

    return parsed


