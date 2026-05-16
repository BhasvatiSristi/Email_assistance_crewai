"""CrewAI Agent factory functions.

Each function returns a properly configured crewai.Agent instance.
"""

from __future__ import annotations

import os
from crewai import Agent, LLM


def _get_llm(model: str = "llama-3.1-8b-instant") -> LLM:
    """Create and return an LLM instance with proper model string formatting."""
    if "/" not in model:
        provider = os.getenv("MODEL_PROVIDER", "groq")
        model = f"{provider}/{model}"
    return LLM(model=model, temperature=0.2)


def create_summarizer_agent(model: str = "llama-3.1-8b-instant") -> Agent:
    """Create a CrewAI Summarizer Agent."""
    return Agent(
        role="Email Summarizer",
        goal="Summarize emails into 2-3 concise, professional bullet points.",
        backstory="You are an expert at extracting key information from emails and presenting it clearly.",
        llm=_get_llm(model),
        verbose=False,
    )


def create_importance_agent(model: str = "llama-3.1-8b-instant") -> Agent:
    """Create a CrewAI Importance Detection Agent."""
    return Agent(
        role="Importance Classifier",
        goal="Classify email importance as HIGH, MEDIUM, or LOW with clear reasoning.",
        backstory="You are skilled at assessing email urgency and business impact.",
        llm=_get_llm(model),
        verbose=False,
    )


def create_action_extractor_agent(model: str = "llama-3.1-8b-instant") -> Agent:
    """Create a CrewAI Action Extraction Agent."""
    return Agent(
        role="Action Item Extractor",
        goal="Extract all action items, deadlines, and tasks from emails.",
        backstory="You are excellent at identifying what needs to be done and by when.",
        llm=_get_llm(model),
        verbose=False,
    )
