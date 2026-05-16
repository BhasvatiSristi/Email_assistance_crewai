"""Helpers to parse CrewAI text responses into JSON safely."""

from __future__ import annotations

import json
import re
from typing import Any, Dict


class ParseError(Exception):
    """Raised when task output cannot be converted into the expected JSON format."""


def _extract_json_block(text: str) -> str:
    """Extract JSON from plain text or markdown code fences."""
    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)

    object_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if object_match:
        return object_match.group(0)

    raise ParseError("No JSON object found in model output.")


def parse_json_output(raw_text: str) -> Dict[str, Any]:
    """Parse model output into a dictionary with clear errors for debugging."""
    json_text = _extract_json_block(raw_text.strip())
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ParseError(f"Invalid JSON output: {exc}") from exc

    if not isinstance(data, dict):
        raise ParseError("Parsed output is not a JSON object.")

    return data
