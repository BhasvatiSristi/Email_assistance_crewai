# AI Email Intelligence Assistant - V1 (Backend Only)

This project is a clean, modular V1 backend for an AI Email Intelligence Assistant built with Python + CrewAI.

It focuses only on the AI workflow and terminal output.

## 1) Why this architecture?

V1 is designed for growth. You will later add FastAPI, notifications, Chrome extension, and dashboard. To support that, each responsibility is separated now:

- `services/`: data access and parsing logic
- `agents/`: CrewAI agent definitions
- `tasks/`: CrewAI task definitions
- `crews/`: workflow orchestration
- `config/`: environment and prompt contracts
- `tools/`: output formatting utilities
- `main.py`: app entry point

This keeps your core AI logic reusable when you move to API routes or background jobs.

## 2) Folder structure

```text
project/
├── agents/
│   ├── __init__.py
│   └── factory.py
├── tasks/
│   ├── __init__.py
│   └── email_tasks.py
├── tools/
│   ├── __init__.py
│   └── output_formatter.py
├── services/
│   ├── __init__.py
│   ├── email_service.py
│   └── parser_service.py
├── config/
│   ├── __init__.py
│   ├── prompts.py
│   └── settings.py
├── crews/
│   ├── __init__.py
│   └── email_intelligence_crew.py
├── .env.example
├── requirements.txt
├── main.py
└── README.md
```

## 3) V1 features covered

1. Email summarization into 2-3 bullets
2. Importance detection (`HIGH`, `MEDIUM`, `LOW`) + reason
3. Classification (`PROFESSIONAL`, `PERSONAL`)
4. Action extraction (deadlines, meetings, required tasks, response requests)
5. Clear terminal output

## 4) Agent design (CrewAI)

The workflow uses 4 agents:

1. Summarizer Agent
2. Importance Detection Agent
3. Classification Agent
4. Action Item Extraction Agent

All agents are deterministic in scope and return JSON-compatible output contracts for easier downstream parsing.

## 5) Step-by-step setup

### Step A: Activate your conda environment

From workspace root:

```powershell
conda activate crewai_env
```

### Step B: Move into project folder

```powershell
cd d:\Projects\crewai_project\project
```

### Step C: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step D: Create your `.env`

Copy `.env.example` to `.env` and set values:

```env
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
MAX_MOCK_EMAILS=3
OPENAI_API_KEY=your_key_here
```

You can switch provider:

- OpenAI: set `MODEL_PROVIDER=openai` and `OPENAI_API_KEY`
- Groq: set `MODEL_PROVIDER=groq` and `GROQ_API_KEY`
- Gemini: set `MODEL_PROVIDER=gemini` and `GOOGLE_API_KEY`

### Step E: Run

```powershell
python main.py
```

## 6) CrewAI installation guide (quick)

If you only want minimal install commands:

```powershell
pip install crewai python-dotenv litellm rich
```

Recommended for reproducibility: use `pip install -r requirements.txt`.

## 7) How the main workflow works

1. Load environment settings from `config/settings.py`
2. Fetch mock emails from `services/email_service.py`
3. Build crew from `crews/email_intelligence_crew.py`
4. Run four tasks sequentially for each email
5. Parse each task output into JSON (`services/parser_service.py`)
6. Print structured analysis in terminal (`tools/output_formatter.py`)

## 8) Mock email testing data

Sample emails include:

- Internship interview invitation with deadline
- Family lunch planning email
- Security audit request with meeting and documents deadline

These are in `services/email_service.py` and can be expanded anytime.

## 9) Error handling strategy

- Missing API key validation at startup
- Safe JSON parsing with explicit parse errors
- Per-email exception isolation (one failure does not stop full batch)

## 10) Future scalability suggestions

1. FastAPI integration:
   - Move `main.py` orchestration into a service class
   - Expose `/analyze-email` and `/analyze-batch` endpoints

2. Gmail integration:
   - Add `services/gmail_service.py`
   - Keep same `EmailMessage` dataclass as shared schema

3. Notifications:
   - Add `services/notification_service.py` with adapters for Telegram/Discord

4. Storage:
   - Add DB layer (SQLite/PostgreSQL) for historical analysis

5. UI support:
   - Keep output model stable so React dashboard can consume JSON directly

## 11) Notes

- V1 currently uses mock emails only.
- Frontend and Chrome extension are intentionally excluded in this phase.
