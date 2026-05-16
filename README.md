# AI Email Intelligence Assistant — V1 (Backend Only)

Lightweight backend to extract concise, actionable intelligence from emails using CrewAI and an LLM provider.

This repository focuses on a simple, testable backend workflow (no frontend). It supports:
- Summarization (2–3 bullets)
- Importance classification (HIGH/MEDIUM/LOW)
- Action-item extraction (simple strings)
- Optional Gmail ingestion (OAuth)
- Optional Slack notifications (webhook)

Contents
- `main.py` — entrypoint that builds a Crew and runs tasks per email
- `agents_factory.py` — CrewAI agent factories
- `tasks_factory.py` — CrewAI task factories
- `email_intelligence_crew.py` — Crew builder that assembles agents + tasks
- `output_formatter.py` — concise CLI output
- `services/` — data & helper services (email mocks, Gmail, parser, notification)
- `gmail_runner.py` — small runner to test Gmail fetch separately
- `requirements.txt` — Python deps

Prerequisites
- Python 3.11
- Conda recommended: the repo includes a `crewai_env` conda environment layout (optional)

Install
1. Create / activate environment (example using conda):

```powershell
conda create -n crewai_env python=3.11 -y
conda activate crewai_env
pip install -r requirements.txt
```

2. (Optional) If you already have a working `crewai` environment, skip environment creation.

Configuration (.env)
Create a `.env` file in the project root (a sample `.env.example` is provided). Important variables:

```
# Model / CrewAI
MODEL_PROVIDER=groq
MODEL_NAME=llama-3.1-8b-instant

# Use Gmail instead of mock emails
USE_GMAIL=false
# Path to OAuth client credentials (download from Google Cloud Console)
GMAIL_CREDENTIALS_FILE=credentials.json
# Token file will be created after first OAuth consent
GMAIL_TOKEN_FILE=token.json

# Notifications
USE_NOTIFY=false
NOTIFY_PROVIDER=slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ

# Rate-limit / token usage mitigations
MAX_EMAIL_BODY_CHARS=2000
SLEEP_BETWEEN_REQUESTS=1.0

# Misc
MAX_MOCK_EMAILS=3
```

Gmail setup (one-time)
1. Go to Google Cloud Console → APIs & Services → Credentials.
2. Create OAuth 2.0 Client ID → Application type: Desktop app.
3. Download the JSON and save it as `credentials.json` in the project root (this file is ignored by `.gitignore`).
4. Run the test runner to perform the OAuth consent flow and save `token.json`:

```powershell
conda run -p crewai_env python gmail_runner.py
```

You will be prompted to authorize in your browser. `token.json` will be saved for future runs.

Running the assistant

- To run against mock emails (default):

```powershell
conda run -p crewai_env python main.py
```

- To run against Gmail (after setting credentials and `USE_GMAIL=true`):

```powershell
set USE_GMAIL=true      # or update .env
conda run -p crewai_env python main.py
```

Notifications
- Slack webhook is supported. Set `USE_NOTIFY=true` and `SLACK_WEBHOOK_URL`.
- Notifications are sent after each email is processed — failures are logged but do not stop processing.

Design notes
- The app uses `crewai.Crew` to orchestrate three agents (summarizer, importance, action extractor) and corresponding tasks. Agents are built in `agents_factory.py` and tasks in `tasks_factory.py`.
- `services/parser_service.py` robustly extracts JSON blocks from LLM output and raises clear parse errors.
- Token usage protections:
  - `MAX_EMAIL_BODY_CHARS` truncates long email bodies before sending to the LLM.
  - `SLEEP_BETWEEN_REQUESTS` adds a pause between requests to avoid tokens-per-minute (TPM) limits.

Troubleshooting
- Groq/OpenAI rate limit errors (e.g., TPM exceeded):
  - Lower `MAX_EMAIL_BODY_CHARS` (e.g., 1000).
  - Increase `SLEEP_BETWEEN_REQUESTS` (2–5s).
  - Use a smaller model or upgrade provider plan.

- `ModuleNotFoundError: No module named 'crewai'`:
  - Install `crewai` in the environment: `pip install crewai`.

- Gmail OAuth errors:
  - Ensure `GMAIL_CREDENTIALS_FILE` points to a valid OAuth client JSON and that Gmail API is enabled for the project.

Development tips
- To test Gmail fetch only, use `gmail_runner.py` so you don't run CrewAI or use provider tokens.
- To add another notification provider (Discord, Teams, SMS), extend `services/notification_service.py` with a new branch.

Project status and next steps
- V1 (backend) implemented with mock + Gmail ingestion and Slack notifications.
- Next logical steps: expose an HTTP endpoint (FastAPI), persist results to a DB, add authentication for multi-user support.

License / Security
- Do NOT commit `credentials.json`, `token.json`, or `.env` — they are ignored in `.gitignore`.

If you want, I can add a short Quickstart section tailored to your OS or create a sample `.env` with placeholders.
