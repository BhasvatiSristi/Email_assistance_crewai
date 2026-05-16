"""CrewAI Task factory functions for Email Intelligence.

Each function returns a properly configured crewai.Task instance.
"""

from __future__ import annotations

from crewai import Task


def create_summary_task(agent) -> Task:
    """Create a task for summarizing an email."""
    return Task(
        description=(
            "Summarize the following email into 2-3 concise bullet points:\n\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n\n"
            "Email Body:\n{body}\n\n"
            "Return ONLY a valid JSON object with key `summary_bullets` (array of 2-3 strings)."
        ),
        expected_output=(
            "A valid JSON object with `summary_bullets` key containing an array of exactly 2-3 concise bullet strings."
        ),
        agent=agent,
    )


def create_importance_task(agent) -> Task:
    """Create a task for determining email importance."""
    return Task(
        description=(
            "Determine the importance level of this email (HIGH, MEDIUM, or LOW):\n\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n\n"
            "Email Body:\n{body}\n\n"
            "Return ONLY a valid JSON object with keys `importance` (HIGH/MEDIUM/LOW) and `why_important` (short reason)."
        ),
        expected_output=(
            "A valid JSON object with `importance` (HIGH/MEDIUM/LOW) and `why_important` keys."
        ),
        agent=agent,
    )


def create_action_task(agent) -> Task:
    """Create a task for extracting action items."""
    return Task(
        description=(
            "Extract all action items, deadlines, and tasks from this email:\n\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n\n"
            "Email Body:\n{body}\n\n"
            "Return ONLY a valid JSON object with key `action_items` (array of simple strings, no nested objects)."
        ),
        expected_output=(
            "A valid JSON object with `action_items` key containing an array of simple action strings."
        ),
        agent=agent,
    )
