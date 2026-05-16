"""Email Intelligence Assistant V1 - uses CrewAI.

Prints concise email analysis:
- EMAIL SUBJECT
- SUMMARY (2-3 bullets)
- IMPORTANCE
- ACTION ITEMS
"""

from __future__ import annotations

import os
import json
from typing import Any, Dict, List

from dotenv import load_dotenv

from services.email_service import EmailMessage, fetch_mock_emails
from services.gmail_service import fetch_gmail_emails
from services.parser_service import ParseError, parse_json_output
from output_formatter import print_concise_email
from services.notification_service import notify
from email_intelligence_crew import build_email_intelligence_crew
import time

load_dotenv()


def _extract_crew_results(crew_result: Any) -> Dict[str, Any]:
    """Extract task outputs from CrewAI crew execution result."""
    results = {
        "summary": {},
        "importance": {},
        "actions": {},
    }

    # Crew result can have tasks_output attribute
    if hasattr(crew_result, "tasks_output") and crew_result.tasks_output:
        task_outputs = crew_result.tasks_output
        if len(task_outputs) > 0:
            try:
                results["summary"] = parse_json_output(str(task_outputs[0].raw or task_outputs[0]))
            except (ParseError, AttributeError, IndexError):
                pass

        if len(task_outputs) > 1:
            try:
                results["importance"] = parse_json_output(str(task_outputs[1].raw or task_outputs[1]))
            except (ParseError, AttributeError, IndexError):
                pass

        if len(task_outputs) > 2:
            try:
                results["actions"] = parse_json_output(str(task_outputs[2].raw or task_outputs[2]))
            except (ParseError, AttributeError, IndexError):
                pass

    # Fallback: crew_result might be a string
    elif isinstance(crew_result, str):
        try:
            data = json.loads(crew_result)
            results["summary"] = data.get("summary", {})
            results["importance"] = data.get("importance", {})
            results["actions"] = data.get("actions", {})
        except json.JSONDecodeError:
            pass

    return results


def main() -> None:
    max_items = int(os.getenv("MAX_MOCK_EMAILS", "3"))
    emails: List[EmailMessage] = fetch_mock_emails(max_items=max_items)

    if not emails:
        print("No emails to analyze.")
        return

    model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
    # Mitigation settings to reduce tokens per minute
    max_body_chars = int(os.getenv("MAX_EMAIL_BODY_CHARS", "2000"))
    sleep_between_requests = float(os.getenv("SLEEP_BETWEEN_REQUESTS", "1.0"))

    # Build the crew once (fail gracefully if crewai is not installed)
    try:
        crew = build_email_intelligence_crew(model=model_name)
    except ModuleNotFoundError as exc:
        print("crewai package not found. Install crewai in your environment to run the agents.")
        print("Run: pip install crewai")
        return

    use_gmail = os.getenv("USE_GMAIL", "false").lower() in ("1", "true", "yes")
    if use_gmail:
        print("Using Gmail as email source (USE_GMAIL=true)")
        emails = fetch_gmail_emails(max_items=max_items)
    else:
        emails = fetch_mock_emails(max_items=max_items)

    for email in emails:
        try:
            # Truncate long email bodies to reduce token usage
            body = email.body or ""
            if len(body) > max_body_chars:
                body = body[:max_body_chars] + "\n\n[truncated]"

            # Execute crew with email data as input
            crew_result = crew.kickoff(
                inputs={
                    "subject": email.subject,
                    "sender": email.sender,
                    "body": body,
                }
            )

            results = _extract_crew_results(crew_result)

            # Extract and normalize summary
            summary = results["summary"].get("summary_bullets", [])
            if not isinstance(summary, list):
                summary = []
            if len(summary) > 3:
                first_two = summary[:2]
                third = " ".join(s.strip() for s in summary[2:])
                summary = first_two + [third]

            # Extract and normalize importance
            importance = "UNKNOWN"
            if isinstance(results["importance"], dict):
                importance = results["importance"].get("importance", "UNKNOWN")
                if isinstance(importance, str):
                    importance = importance.strip().upper()

            # Extract and normalize action items
            action_items = []
            if isinstance(results["actions"], dict):
                raw_actions = results["actions"].get("action_items", [])
                if isinstance(raw_actions, list):
                    for item in raw_actions:
                        if isinstance(item, dict):
                            desc = item.get("description", "")
                            deadline = item.get("deadline", "")
                            if desc and deadline:
                                action_items.append(f"{desc} by {deadline}")
                            elif desc:
                                action_items.append(desc)
                        elif isinstance(item, str):
                            action_items.append(item)

            print_concise_email(email.subject, summary, importance, action_items)

            # Send notification if enabled
            use_notify = os.getenv("USE_NOTIFY", "false").lower() in ("1", "true", "yes")
            if use_notify:
                try:
                    ok = notify(email.subject, summary, importance, action_items)
                    if not ok:
                        print(f"[warning] notification failed for: {email.subject}")
                except Exception as exc:
                    print(f"[warning] notification error: {exc}")

            # Throttle to avoid exceeding tokens-per-minute limits
            if sleep_between_requests > 0:
                time.sleep(sleep_between_requests)

        except (RuntimeError, ParseError) as exc:
            print_concise_email(email.subject, [], "UNKNOWN", [])
            print(f"[warning] {exc}")

        except Exception as exc:
            print_concise_email(email.subject, [], "UNKNOWN", [])
            print(f"[unexpected error] {exc}")


if __name__ == "__main__":
    main()