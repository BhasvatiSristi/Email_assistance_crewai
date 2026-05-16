"""Email Intelligence Crew - assembles agents and tasks into a working crew."""

from __future__ import annotations

from crewai import Crew, Process

from agents_factory import (
    create_summarizer_agent,
    create_importance_agent,
    create_action_extractor_agent,
)
from tasks_factory import (
    create_summary_task,
    create_importance_task,
    create_action_task,
)


def build_email_intelligence_crew(model: str = "llama-3.1-8b-instant") -> Crew:
    """Build and return the Email Intelligence Crew."""
    
    # Create agents
    summarizer_agent = create_summarizer_agent(model=model)
    importance_agent = create_importance_agent(model=model)
    action_agent = create_action_extractor_agent(model=model)

    # Create tasks
    summary_task = create_summary_task(summarizer_agent)
    importance_task = create_importance_task(importance_agent)
    action_task = create_action_task(action_agent)

    # Assemble crew
    return Crew(
        agents=[summarizer_agent, importance_agent, action_agent],
        tasks=[summary_task, importance_task, action_task],
        process=Process.sequential,
        verbose=False,
    )
