"""Email data layer. V1 uses in-memory mock emails; Gmail integration can be added later."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EmailMessage:
    subject: str
    sender: str
    body: str


MOCK_EMAILS: List[EmailMessage] = [
    EmailMessage(
        subject="Internship Interview Invitation",
        sender="hr@innovatek.com",
        body=(
            "Hi Rahul, we are pleased to invite you for the internship technical interview "
            "on Monday at 10:00 AM IST via Google Meet. Please submit your updated resume "
            "and latest transcript by Sunday 6:00 PM. The panel will include two engineers "
            "and one hiring manager. Kindly confirm your availability by replying to this email "
            "before Saturday evening."
        ),
    ),
    EmailMessage(
        subject="Weekend Family Lunch",
        sender="mom@example.com",
        body=(
            "Hey! We are planning a family lunch this Sunday around 1 PM at grandma's place. "
            "If you can, bring the dessert you made last time because everyone loved it. "
            "Please let me know by Friday if you can make it so we can plan groceries."
        ),
    ),
    EmailMessage(
        subject="Quarterly Security Audit Documents Required",
        sender="it-compliance@company.com",
        body=(
            "Hello Team, this is a reminder that the quarterly security audit starts next Wednesday. "
            "Please upload system access logs, vendor access reports, and incident closure notes "
            "to the compliance folder by Tuesday 4 PM. Missing documents may delay certification. "
            "A review meeting is scheduled on Wednesday at 11 AM in Conference Room B."
        ),
    ),
]


def fetch_mock_emails(max_items: int = 5) -> List[EmailMessage]:
    """Return a limited set of mock emails for local development and testing."""
    return MOCK_EMAILS[:max_items]
