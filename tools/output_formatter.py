"""Terminal output formatting for readable AI analysis results."""

from __future__ import annotations

from typing import Any, Dict, List


def _print_list(title: str, items: List[str]) -> None:
    print(f"{title}:")
    if not items:
        print("- None")
        return

    for item in items:
        print(f"- {item}")


def print_email_analysis(email_subject: str, result: Dict[str, Any]) -> None:
    """Print analysis in a consistent format for CLI usage and future API responses."""
    summary_bullets = result.get("summary", {}).get("summary_bullets", [])
    category = result.get("classification", {}).get("category", "UNKNOWN")
    importance = result.get("importance", {}).get("importance", "UNKNOWN")
    why_important = result.get("importance", {}).get("why_important", "Not provided")

    action_items = result.get("actions", {})
    deadlines = action_items.get("deadlines", [])
    meetings = action_items.get("meetings", [])
    required_tasks = action_items.get("required_tasks", [])
    response_requests = action_items.get("response_requests", [])

    print("=" * 72)
    print(f"EMAIL SUBJECT: {email_subject}")
    print()

    _print_list("SUMMARY", summary_bullets)
    print()

    print("CATEGORY:")
    print(category)
    print()

    print("IMPORTANCE:")
    print(importance)
    print()

    print("WHY IMPORTANT:")
    print(why_important)
    print()

    print("ACTION ITEMS:")
    _print_list("DEADLINES", deadlines)
    _print_list("MEETINGS", meetings)
    _print_list("REQUIRED TASKS", required_tasks)
    _print_list("RESPONSE REQUESTS", response_requests)
    print("=" * 72)
