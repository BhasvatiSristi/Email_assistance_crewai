"""Agent factory module to keep agent definitions reusable and testable."""

from __future__ import annotations

from crewai import Agent


def build_summarizer_agent(model: str) -> Agent:
    return Agent(
        role="Email Summarizer",
        goal="Summarize long emails into 2-3 concise, professional bullets while preserving key details.",
        backstory=(
            "You are an executive communication assistant focused on high-signal summaries. "
            "You never add facts that are not present in the original email."
        ),
        llm=model,
        allow_delegation=False,
        verbose=False,
    )


def build_importance_agent(model: str) -> Agent:
    return Agent(
        role="Importance Detection Specialist",
        goal="Classify each email's urgency as HIGH, MEDIUM, or LOW and explain why.",
        backstory=(
            "You are skilled at urgency analysis in workplace and personal communication, "
            "considering deadlines, business impact, and explicit response requests."
        ),
        llm=model,
        allow_delegation=False,
        verbose=False,
    )


def build_classification_agent(model: str) -> Agent:
    return Agent(
        role="Email Classification Analyst",
        goal="Classify whether an email is PROFESSIONAL or PERSONAL with a short reason.",
        backstory=(
            "You maintain strict taxonomy discipline and avoid ambiguous outputs. "
            "You always pick one category only."
        ),
        llm=model,
        allow_delegation=False,
        verbose=False,
    )


def build_action_extractor_agent(model: str) -> Agent:
    return Agent(
        role="Action Item Extraction Specialist",
        goal="Extract deadlines, meetings, required tasks, and response requests.",
        backstory=(
            "You parse operational commitments from natural language emails and produce "
            "clear action lists for productivity workflows."
        ),
        llm=model,
        allow_delegation=False,
        verbose=False,
    )
