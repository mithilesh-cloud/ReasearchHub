# ResearchHub

A lightweight FastAPI backend scaffold for collaborative research workflows.

## Features
- JWT-based auth (register/login)
- Workspaces per user
- Paper storage + semantic-ish search placeholder
- Chat endpoint that builds prompt context from saved papers
- SQLAlchemy models and SQLite default persistence

## Project layout
```text
app/
├── main.py
├── core/
├── database/
├── models/
├── routers/
├── schemas/
├── services/
└── utils/
```

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic-settings python-jose passlib[bcrypt] email-validator
uvicorn app.main:app --reload
```

Open API docs at `http://127.0.0.1:8000/docs`.
