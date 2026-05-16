"""Application settings and environment loading for Email Intelligence Assistant V1."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


load_dotenv()


SUPPORTED_PROVIDERS = {"openai", "groq", "gemini"}


@dataclass(frozen=True)
class AppSettings:
    """Centralized runtime settings for easy future FastAPI integration."""

    model_provider: str
    model_name: str
    max_mock_emails: int


def get_settings() -> AppSettings:
    """Read app settings from environment variables with safe defaults."""
    provider = os.getenv("MODEL_PROVIDER", "openai").strip().lower()
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini").strip()
    max_mock_emails = int(os.getenv("MAX_MOCK_EMAILS", "5"))

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported MODEL_PROVIDER '{provider}'. "
            f"Use one of: {', '.join(sorted(SUPPORTED_PROVIDERS))}."
        )

    return AppSettings(
        model_provider=provider,
        model_name=model_name,
        max_mock_emails=max_mock_emails,
    )


def get_crewai_model_string(settings: AppSettings) -> str:
    """
    Build LiteLLM model string used by CrewAI.

    Examples:
    - openai/gpt-4o-mini
    - groq/llama-3.1-8b-instant
    - gemini/gemini-1.5-flash
    """
    return f"{settings.model_provider}/{settings.model_name}"


def validate_required_env(settings: AppSettings) -> List[str]:
    """Return a list of missing environment variables required by the chosen provider."""
    missing: List[str] = []

    if settings.model_provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    elif settings.model_provider == "groq" and not os.getenv("GROQ_API_KEY"):
        missing.append("GROQ_API_KEY")
    elif settings.model_provider == "gemini" and not os.getenv("GOOGLE_API_KEY"):
        missing.append("GOOGLE_API_KEY")

    return missing
