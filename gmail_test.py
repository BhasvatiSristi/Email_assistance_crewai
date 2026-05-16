from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)

    return service


def get_email_body(payload):
    body = ""

    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType')

            if mime_type == 'text/plain':
                data = part['body'].get('data')

                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    return body

    else:
        data = payload['body'].get('data')

        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')

    return body


def fetch_emails(service):
    results = service.users().messages().list(
        userId='me',
        maxResults=5,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])

    for msg in messages:
        message = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        payload = message['payload']
        headers = payload['headers']

        subject = ""
        sender = ""

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']

            if header['name'] == 'From':
                sender = header['value']

        body = get_email_body(payload)

        print("\n" + "="*60)
        print("SUBJECT:", subject)
        print("FROM:", sender)
        print("BODY:\n")
        print(body[:1000])
        print("="*60)


if __name__ == "__main__":
    service = authenticate_gmail()
    fetch_emails(service)