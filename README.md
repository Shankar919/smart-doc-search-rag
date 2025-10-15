# AI Search — FastAPI + Qdrant + ChatGPT (Starter)

This is a ready-to-run starter repository for a Retrieval-Augmented Generation (RAG)
knowledge search engine using **FastAPI**, **Qdrant** (vector DB), and **OpenAI ChatGPT**
for answer synthesis. It also supports local SentenceTransformers embeddings.

## Features
- Ingest PDFs / TXT files, chunk text, create embeddings
- Index embeddings into Qdrant
- FastAPI endpoints for `/ingest` and `/query`
- Streamlit demo frontend for upload + ask flow
- `.env.example` with configuration

## Quick start (local)
1. Clone or unzip this repo.
2. Create and activate a Python 3.10+ virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   venv\Scripts\activate     # Windows (PowerShell)
   pip install -r requirements.txt
   ```
3. Fill `.env` from `.env.example` (set OPENAI_API_KEY if you want ChatGPT synthesis).
4. Start Qdrant locally (Docker):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
5. Start the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
6. Start the demo frontend in another terminal:
   ```bash
   streamlit run demo/streamlit_frontend.py
   ```

## Files & structure
- `app/` — backend code: ingestion, qdrant wrapper, embeddings, synth
- `demo/` — simple Streamlit UI
- `.env.example` — environment variables to set
- `requirements.txt` — Python dependencies

## Notes
- By default this supports local sentence-transformers embeddings (`all-MiniLM-L6-v2`).
  If you set `OPENAI_API_KEY`, the repo will prefer OpenAI embeddings for the query path.
- The synthesis step uses OpenAI Chat Completion (ChatGPT). If you don't supply an API key,
  synth will fallback to returning concatenated snippets.
- This is a starter template — consider adding auth, persistence for metadata, re-ranking,
  and improved UI for production use.
