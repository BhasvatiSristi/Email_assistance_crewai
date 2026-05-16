"""Crew assembly for Email Intelligence Assistant V1."""

from __future__ import annotations

from typing import Any, Dict

from crewai import Crew, Process

from agents.factory import (
    build_action_extractor_agent,
    build_classification_agent,
    build_importance_agent,
    build_summarizer_agent,
)
from tasks.email_tasks import (
    create_action_extraction_task,
    create_classification_task,
    create_importance_task,
    create_summary_task,
)


def build_email_intelligence_crew(model: str) -> Crew:
    """Build the multi-agent CrewAI pipeline."""
    summarizer_agent = build_summarizer_agent(model)
    importance_agent = build_importance_agent(model)
    classification_agent = build_classification_agent(model)
    action_agent = build_action_extractor_agent(model)

    summary_task = create_summary_task(summarizer_agent)
    importance_task = create_importance_task(importance_agent)
    classification_task = create_classification_task(classification_agent)
    action_task = create_action_extraction_task(action_agent)

    return Crew(
        agents=[
            summarizer_agent,
            importance_agent,
            classification_agent,
            action_agent,
        ],
        tasks=[summary_task, importance_task, classification_task, action_task],
        process=Process.sequential,
        verbose=False,
    )


def run_email_intelligence(crew: Crew, email_payload: Dict[str, Any]):
    """Execute crew workflow for one email payload."""
    return crew.kickoff(inputs=email_payload)
