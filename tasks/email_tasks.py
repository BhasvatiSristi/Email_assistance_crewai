"""Task definitions for the Email Intelligence Assistant Crew."""

from __future__ import annotations

from crewai import Task

from config.prompts import (
    ACTION_OUTPUT_CONTRACT,
    CLASSIFICATION_OUTPUT_CONTRACT,
    IMPORTANCE_OUTPUT_CONTRACT,
    SUMMARY_OUTPUT_CONTRACT,
)


def create_summary_task(agent) -> Task:
    return Task(
        description=(
            "Analyze the following email and summarize it into 2-3 concise bullet points.\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n"
            "Email Body: {body}\n"
            "Rules: Keep details factual, concise, and professional."
        ),
        expected_output=SUMMARY_OUTPUT_CONTRACT,
        agent=agent,
    )


def create_importance_task(agent) -> Task:
    return Task(
        description=(
            "Determine importance of this email as HIGH, MEDIUM, or LOW.\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n"
            "Email Body: {body}\n"
            "Return the level and a short why_important reason."
        ),
        expected_output=IMPORTANCE_OUTPUT_CONTRACT,
        agent=agent,
    )


def create_classification_task(agent) -> Task:
    return Task(
        description=(
            "Classify this email as PROFESSIONAL or PERSONAL.\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n"
            "Email Body: {body}\n"
            "Return only one category with a short reason."
        ),
        expected_output=CLASSIFICATION_OUTPUT_CONTRACT,
        agent=agent,
    )


def create_action_extraction_task(agent) -> Task:
    return Task(
        description=(
            "Extract all action-oriented information from this email.\n"
            "Email Subject: {subject}\n"
            "Sender: {sender}\n"
            "Email Body: {body}\n"
            "Extract deadlines, meetings, required_tasks, response_requests."
        ),
        expected_output=ACTION_OUTPUT_CONTRACT,
        agent=agent,
    )
