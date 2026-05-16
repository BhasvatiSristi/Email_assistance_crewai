"""Standalone runner to test Gmail fetch without importing CrewAI.

Run this to verify the `services.gmail_service.fetch_gmail_emails` function.
"""

from services.gmail_service import fetch_gmail_emails


if __name__ == "__main__":
    emails = fetch_gmail_emails(max_items=3)
    if not emails:
        print("No emails fetched.")
    else:
        for i, e in enumerate(emails, 1):
            print(f"#{i}")
            print(f"Subject: {e.subject}")
            print(f"From: {e.sender}")
            print(f"Body (first 200 chars): {e.body[:200]!s}")
            print()
