"""Prompt snippets and shared output contracts for agent tasks."""

SUMMARY_OUTPUT_CONTRACT = """
Return valid JSON with this exact schema:
{
  "summary_bullets": ["bullet 1", "bullet 2", "bullet 3 (optional)"]
}
""".strip()

IMPORTANCE_OUTPUT_CONTRACT = """
Return valid JSON with this exact schema:
{
  "importance": "HIGH | MEDIUM | LOW",
  "why_important": "Short reason"
}
""".strip()

CLASSIFICATION_OUTPUT_CONTRACT = """
Return valid JSON with this exact schema:
{
  "category": "PROFESSIONAL | PERSONAL",
  "reason": "Short reason"
}
""".strip()

ACTION_OUTPUT_CONTRACT = """
Return valid JSON with this exact schema:
{
  "deadlines": ["..."] ,
  "meetings": ["..."] ,
  "required_tasks": ["..."] ,
  "response_requests": ["..."]
}
Use empty arrays when no items exist.
""".strip()
