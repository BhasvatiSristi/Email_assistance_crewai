"""Notification service supporting multiple providers (Slack implemented).

Environment variables:
- NOTIFY_PROVIDER=slack
- SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
"""

from __future__ import annotations

import os
from typing import List

import requests


def _format_message(subject: str, summary: List[str], importance: str, actions: List[str]) -> str:
    lines = []
    lines.append(f"*EMAIL SUBJECT:* {subject}")
    lines.append("")
    lines.append("*SUMMARY:*")
    if summary:
        for b in summary:
            lines.append(f"• {b}")
    else:
        lines.append("• None")

    lines.append("")
    lines.append(f"*IMPORTANCE:* {importance}")

    lines.append("")
    lines.append("*ACTION ITEMS:*")
    if actions:
        for a in actions:
            lines.append(f"• {a}")
    else:
        lines.append("• None")

    return "\n".join(lines)


def _send_slack(webhook_url: str, text: str) -> bool:
    try:
        resp = requests.post(webhook_url, json={"text": text}, timeout=5)
        resp.raise_for_status()
        return True
    except Exception:
        return False


def notify(subject: str, summary: List[str], importance: str, actions: List[str]) -> bool:
    provider = os.getenv("NOTIFY_PROVIDER", "slack").lower()
    if provider == "slack":
        webhook = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook:
            raise RuntimeError("SLACK_WEBHOOK_URL not set for Slack notifications")
        text = _format_message(subject, summary, importance, actions)
        return _send_slack(webhook, text)

    raise RuntimeError(f"Unsupported notify provider: {provider}")
