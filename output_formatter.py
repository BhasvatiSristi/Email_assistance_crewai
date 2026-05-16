"""Minimal terminal formatter: concise output only.

Prints exactly:
- Email subject
- Summary (2-3 bullets)
- Importance
- Action items list

Designed to be compact for CLI consumption and easy parsing by other tools.
"""

from __future__ import annotations

from typing import List


def print_concise_email(subject: str, summary: List[str], importance: str, actions: List[str]) -> None:
    print("---")
    print(f"EMAIL SUBJECT: {subject}")
    print()
    print("SUMMARY:")
    if not summary:
        print("- None")
    else:
        for b in summary:
            print(f"- {b}")

    print()
    print("IMPORTANCE:")
    print(importance)

    print()
    print("ACTION ITEMS:")
    if not actions:
        print("- None")
    else:
        for a in actions:
            print(f"- {a}")
    print("---")
