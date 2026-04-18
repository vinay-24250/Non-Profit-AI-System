# backend/triage_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools.ner_tool import NERTool
from tools.json_parser_tool import parse_json_output

load_dotenv()

# ── LLM — pass as string with groq/ prefix ────────────────────────────────────
# New CrewAI versions require LLM string or crewai.LLM object, not ChatGroq
def get_llm(temperature: float = 0.2):
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
    )


def _extract_task_output(result, index: int) -> str:
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


def run_triage_agent(email_text: str) -> dict:
    llm = get_llm(temperature=0.2)
    ner = NERTool()

    # Agent 1: Classifier
    classifier = Agent(
        role="Email Triage Specialist",
        goal=(
            "Accurately classify incoming Non-Profit emails by urgency level "
            "and communication intent to enable fast, prioritized responses."
        ),
        backstory=(
            "You are a seasoned Non-Profit communications manager with 10 years "
            "of experience triaging donor, volunteer, and grant inquiries. "
            "You instantly recognize tone, urgency signals, and intent patterns."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Agent 2: NER Extractor
    extractor = Agent(
        role="Data Extraction Specialist",
        goal=(
            "Extract all critical named entities from email text including "
            "donor names, IDs, dates, amounts, and organizations."
        ),
        backstory=(
            "You are a data analyst specializing in Non-Profit CRM systems. "
            "You use NLP tools to pull structured data from unstructured email text."
        ),
        llm=llm,
        tools=[ner],
        verbose=True,
        allow_delegation=False,
    )

    # Agent 3: Responder
    responder = Agent(
        role="Non-Profit Communications Officer",
        goal=(
            "Draft warm, professional, and actionable email responses that "
            "reflect the organization's values and resolve donor concerns quickly."
        ),
        backstory=(
            "You are a compassionate communications officer at a Non-Profit. "
            "You write empathetic, on-brand replies that make donors feel valued."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Task 1: Classify
    classify_task = Task(
        description=(
            "Analyze this incoming Non-Profit email and classify it.\n\n"
            "Email:\n" + email_text + "\n\n"
            "Return ONLY a JSON object with these exact keys:\n"
            "- urgency: one of 'critical', 'high', 'medium', 'low'\n"
            "- intent: one of 'donation_inquiry', 'volunteer_request', "
            "'complaint', 'general_info', 'grant_application', 'media_inquiry'\n"
            "- confidence: float between 0 and 1\n"
            "- reasoning: one concise sentence\n\n"
            "Return ONLY the JSON. No markdown, no explanation."
        ),
        expected_output="A valid JSON object with keys: urgency, intent, confidence, reasoning.",
        agent=classifier,
    )

    # Task 2: Extract Entities
    extract_task = Task(
        description=(
            "Use the Named Entity Recognition Tool to extract all entities "
            "from this email:\n\n" + email_text + "\n\n"
            "Pass the full email text to the NER tool. "
            "Return the raw JSON output from the tool exactly as-is."
        ),
        expected_output=(
            "A valid JSON object with keys: persons, organizations, dates, "
            "amounts, locations, ids — each a list of strings."
        ),
        agent=extractor,
    )

    # Task 3: Draft Response
    draft_task = Task(
        description=(
            "Using the classification and entities from previous tasks, "
            "write a professional draft reply to:\n\n" + email_text + "\n\n"
            "Guidelines:\n"
            "- Be empathetic and warm\n"
            "- Address sender by name if available\n"
            "- Acknowledge their specific concern\n"
            "- Provide one clear actionable next step\n"
            "- Under 150 words, no subject line\n"
            "- No placeholder text like [Name]\n\n"
            "Return only the email body text."
        ),
        expected_output="A professional empathetic draft email reply under 150 words.",
        agent=responder,
    )

    # Run Crew 
    crew = Crew(
        agents=[classifier, extractor, responder],
        tasks=[classify_task, extract_task, draft_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    try:
        classification = parse_json_output(_extract_task_output(result, 0))
    except Exception:
        classification = {
            "urgency": "medium",
            "intent": "general_info",
            "confidence": 0.5,
            "reasoning": "Could not parse classification.",
        }

    try:
        entities = parse_json_output(_extract_task_output(result, 1))
    except Exception:
        entities = {
            "persons": [], "organizations": [], "dates": [],
            "amounts": [], "locations": [], "ids": [],
        }

    try:
        draft = _extract_task_output(result, 2).strip()
    except Exception:
        draft = str(result)

    return {
        "classification": classification,
        "entities":       entities,
        "draft_response": draft,
    }