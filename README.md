# Sujoy Portfolio RAG Chatbot

A Python/FastAPI Retrieval-Augmented Generation (RAG) chatbot for a personal portfolio.

## Stack
- Python 3.11+
- FastAPI + Uvicorn
- ChromaDB
- OpenAI embeddings
- OpenAI Responses API
- Vanilla HTML/CSS/JavaScript frontend

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# Edit .env and add OPENAI_API_KEY
python scripts/ingest.py
uvicorn app.main:app --reload
```

### Frontend
In another terminal:
```bash
cd frontend
python -m http.server 5500
```
Open http://127.0.0.1:5500

The frontend expects the API at http://127.0.0.1:8000.

## Notes
- Never commit `.env`.
- Re-run `python scripts/ingest.py` after changing knowledge files.
- Knowledge files are curated from the portfolio rather than indexing raw HTML.
