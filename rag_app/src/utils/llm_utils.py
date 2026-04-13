import json
import re


def parse_analysis_response(text: str) -> dict:
    """Parse structured JSON from LLM analysis output, with keyword fallback."""
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            return {
                "prediction": parsed.get("prediction", "UNVERIFIABLE").upper(),
                "confidence": float(parsed.get("confidence", 0.5)),
                "explanation": parsed.get("explanation", text),
                "key_claims": parsed.get("key_claims", []),
            }
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    upper = text.upper()
    if "FAKE" in upper and "REAL" not in upper:
        prediction = "FAKE"
    elif "REAL" in upper and "FAKE" not in upper:
        prediction = "REAL"
    elif "MIXED" in upper:
        prediction = "MIXED"
    else:
        prediction = "UNVERIFIABLE"

    return {
        "prediction": prediction,
        "confidence": 0.5,
        "explanation": text.strip(),
        "key_claims": [],
    }
