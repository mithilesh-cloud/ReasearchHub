# ResearchHub AI Backend (FastAPI)

Backend for an AI-powered research paper discovery, workspace management, and contextual chatbot platform.

## Features
- JWT authentication (register/login)
- Workspace creation and listing
- Academic paper search via arXiv API
- One-click paper import into workspaces
- Embedding generation for abstracts (sentence-transformers)
- Vector similarity retrieval for contextual Q&A
- Chat endpoint integrated with Groq Llama 3.3 70B
- CORS enabled for React frontend (`localhost:3000`)

## Project Structure
```
app/
├── main.py
├── core/
│   ├── config.py
│   ├── security.py
├── models/
│   ├── user.py
│   ├── workspace.py
│   ├── paper.py
│   ├── conversation.py
├── schemas/
│   ├── auth.py
│   ├── paper.py
│   ├── chat.py
│   ├── workspace.py
├── routers/
│   ├── auth.py
│   ├── search.py
│   ├── workspace.py
│   ├── chat.py
├── services/
│   ├── embedding_service.py
│   ├── vector_service.py
│   ├── llm_service.py
│   ├── search_service.py
├── database/
│   ├── session.py
└── utils/
    ├── prompt_builder.py
```

## Setup
1. Create environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure environment:
   ```bash
   cp .env.example .env
   ```
3. Run API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Key Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `POST /workspaces`
- `GET /workspaces`
- `POST /papers/search`
- `POST /papers/import`
- `POST /chat`

Use `Authorization: Bearer <token>` for protected routes.
