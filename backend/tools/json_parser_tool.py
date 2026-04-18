# backend/tools/json_parser_tool.py
import re
import json


def parse_json_output(raw: str) -> dict:
    """
    Safely extract a JSON object from LLM output.
    Handles markdown fences, leading/trailing text, and common formatting issues.
    """
    if not raw:
        raise ValueError("Empty output from agent.")

    text = raw.strip()

    # 1. Strip markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    # 2. Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 3. Extract first {...} block from the text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from agent output:\n{raw[:500]}")