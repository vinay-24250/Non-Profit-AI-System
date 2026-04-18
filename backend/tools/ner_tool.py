# backend/tools/ner_tool.py
import re
import json
import spacy

# BaseTool import — compatible across crewai versions
try:
    from crewai.tools import BaseTool          # crewai 0.55+
except ImportError:
    try:
        from crewai_tools import BaseTool      # older crewai
    except ImportError:
        from langchain.tools import BaseTool   # fallback

# Load spaCy model once at import time
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "\n\n❌  spaCy model not found.\n"
        "    Run: python -m spacy download en_core_web_sm\n"
    )


class NERTool(BaseTool):
    name: str = "Named Entity Recognition Tool"
    description: str = (
        "Extracts named entities from text using spaCy NLP. "
        "Identifies persons, organizations, dates, monetary amounts, "
        "locations, and custom IDs (e.g. DON-12345, VOL-8821). "
        "Input: raw email text. Output: JSON string of extracted entities."
    )

    def _run(self, text: str) -> str:
        doc = nlp(text)

        entities = {
            "persons":       [],
            "organizations": [],
            "dates":         [],
            "amounts":       [],
            "locations":     [],
            "ids":           [],
        }

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["persons"].append(ent.text)
            elif ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ in ("DATE", "TIME"):
                entities["dates"].append(ent.text)
            elif ent.label_ == "MONEY":
                entities["amounts"].append(ent.text)
            elif ent.label_ in ("GPE", "LOC"):
                entities["locations"].append(ent.text)

        # Regex: donor/volunteer/grant IDs like DON-20240315, VOL-8821, GRN-4492
        ids = re.findall(r"\b[A-Z]{2,4}-?\d{4,8}\b", text)
        entities["ids"] = list(set(ids))

        # Deduplicate all lists while preserving order
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))

        return json.dumps(entities)