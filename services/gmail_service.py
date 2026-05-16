"""Gmail integration service.

Provides a simple function to fetch recent emails and return
`EmailMessage` objects from `services.email_service`.

Uses OAuth credentials stored in `credentials.json` and `token.json`.
"""

from __future__ import annotations

import os
import base64
from typing import List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from services.email_service import EmailMessage

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE", "token.json")


def _get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service


def _get_body_from_payload(payload: dict) -> str:
    # Prefer plain text part, fallback to first non-empty part
    if not payload:
        return ""

    parts = payload.get("parts")
    if parts:
        for part in parts:
            mime = part.get("mimeType", "")
            if mime == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        # fallback: first part with data
        for part in parts:
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # single-part message
    data = payload.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    return ""


def fetch_gmail_emails(max_items: int = 5) -> List[EmailMessage]:
    """Fetch recent emails from the authenticated Gmail account.

    Returns a list of `EmailMessage` dataclass instances.
    """
    service = _get_gmail_service()
    resp = service.users().messages().list(userId="me", maxResults=max_items, labelIds=["INBOX"]).execute()
    msgs = resp.get("messages", [])
    out: List[EmailMessage] = []
    for m in msgs:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h.get("name", "").lower() == "subject"), "")
        sender = next((h["value"] for h in headers if h.get("name", "").lower() == "from"), "")
        body = _get_body_from_payload(payload)
        out.append(EmailMessage(subject=subject, sender=sender, body=body))

    return out
