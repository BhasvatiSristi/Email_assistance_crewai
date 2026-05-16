"""Entry point for AI Email Intelligence Assistant V1."""

from __future__ import annotations

from typing import Any, Dict, List

from config.settings import get_crewai_model_string, get_settings, validate_required_env
from crews.email_intelligence_crew import build_email_intelligence_crew, run_email_intelligence
from services.email_service import EmailMessage, fetch_mock_emails
from services.parser_service import ParseError, parse_json_output
from tools.output_formatter import print_email_analysis


def _normalize_task_outputs(raw_result: Any) -> List[str]:
    """
    Convert CrewAI result object into a list of task output strings.

    CrewAI versions can return different result objects. This helper keeps the project
    resilient across minor version changes.
    """
    if hasattr(raw_result, "tasks_output") and raw_result.tasks_output:
        normalized = []
        for item in raw_result.tasks_output:
            if hasattr(item, "raw"):
                normalized.append(str(item.raw))
            else:
                normalized.append(str(item))
        return normalized

    # Fallback: when full result is only a final text response.
    return [str(raw_result)]


def _build_email_payload(email: EmailMessage) -> Dict[str, str]:
    return {
        "subject": email.subject,
        "sender": email.sender,
        "body": email.body,
    }


def main() -> None:
    settings = get_settings()
    missing_vars = validate_required_env(settings)

    if missing_vars:
        missing = ", ".join(missing_vars)
        raise RuntimeError(f"Missing required environment variables: {missing}")

    model = get_crewai_model_string(settings)
    crew = build_email_intelligence_crew(model=model)

    emails = fetch_mock_emails(max_items=settings.max_mock_emails)
    if not emails:
        print("No emails found.")
        return

    print(f"Running Email Intelligence Assistant V1 on {len(emails)} email(s)...\n")

    for email in emails:
        payload = _build_email_payload(email)

        try:
            raw_result = run_email_intelligence(crew, payload)
            task_outputs = _normalize_task_outputs(raw_result)

            # Expected order matches the task list in the crew.
            summary = parse_json_output(task_outputs[0]) if len(task_outputs) > 0 else {}
            importance = parse_json_output(task_outputs[1]) if len(task_outputs) > 1 else {}
            classification = parse_json_output(task_outputs[2]) if len(task_outputs) > 2 else {}
            actions = parse_json_output(task_outputs[3]) if len(task_outputs) > 3 else {}

            result = {
                "summary": summary,
                "importance": importance,
                "classification": classification,
                "actions": actions,
            }

            print_email_analysis(email.subject, result)

        except ParseError as exc:
            print("=" * 72)
            print(f"EMAIL SUBJECT: {email.subject}")
            print("Analysis failed while parsing agent output.")
            print(f"Error: {exc}")
            print("=" * 72)
        except Exception as exc:  # Broad catch to keep batch processing robust.
            print("=" * 72)
            print(f"EMAIL SUBJECT: {email.subject}")
            print("Unexpected error while analyzing this email.")
            print(f"Error: {exc}")
            print("=" * 72)


if __name__ == "__main__":
    main()
