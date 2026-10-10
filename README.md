# Nyaya Legal & Compliance RAG Project

Nyaya is a local-first, deterministic retrieval-augmented generation (RAG) project for fictional legal and compliance document analysis. It loads sample documents, redacts personally identifiable information, chunks and embeds the text, stores it in a local vector database, and answers user questions using a mock or OpenAI-compatible LLM.

The project is implemented across the main modules in `app.py`, `agent.py`, `settings.py`, `loaders.py`, `chunking.py`, `embeddings.py`, `vectorstore.py`, `retrieval.py`, `context.py`, `llm_client.py`, and `pii.py`.

## Project purpose

This project is designed to:

- ingest legal/compliance documents in PDF, DOCX, HTML, CSV, and JSON formats
- redact email and phone data before indexing or answering questions
- build semantic chunks for retrieval
- index chunks in ChromaDB locally
- answer grounded questions using a small retrieval context
- enforce guardrails for unsupported or out-of-scope requests
- run as a FastAPI service with a health endpoint and a question-answer endpoint

## What the application does

The main execution flow is:

1. Load documents from a `documents/` folder.
2. Redact sensitive text using `pii.py`.
3. Chunk documents with the strategy selected in `settings.py`.
4. Encode chunks with sentence embeddings.
5. Persist chunks into a local Chroma vectorstore.
6. Retrieve the most relevant chunks for a question.
7. Build context and pass it to the LLM client.
8. Return the answer, source filenames, and metadata through the FastAPI API.

## Project structure

- `app.py` – FastAPI application and HTTP endpoints
- `agent.py` – orchestration logic for indexing and answering questions
- `settings.py` – environment-driven configuration and validation
- `loaders.py` – document ingestion for multiple file types
- `chunking.py` – chunking strategies and document segmentation
- `embeddings.py` – text embedding generation
- `vectorstore.py` – Chroma vector database setup and persistence
- `retrieval.py` – deduplication and context-size filtering
- `context.py` – prompt/context construction and guardrails
- `llm_client.py` – LLM interaction layer
- `pii.py` – PII redaction rules
- `build_vectorstore.py` – creates the local vector index
- `scripts/generate_sample_documents.py` – creates fictional legal/compliance sample docs
- `tests/` – unit tests for ingestion, redaction, retrieval, guardrails, and API behavior

## Requirements

- Python 3.10+
- pip
- An internet connection only for the initial dependency installation, if needed

## Dependency installation

From the project root:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

## Environment configuration

The project reads settings from a local `.env` file using `settings.py`.

Create a `.env` file in the root folder with values such as:

```env
APP_ENV=development
CHROMA_BASE_DIR=./chroma_db
CHUNKING_STRATEGY=heading_aware
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODE=mock
MAX_CONTEXT_CHARS=6000
RETRIEVAL_K=5
TOPK_MIN_SCORE=0.30
THRESHOLD_MIN_SCORE=0.45
NEAR_DUPLICATE_THRESHOLD=0.90
REFERENCE_DATE=2026-10-10
```

For a real LLM integration, set:

```env
LLM_MODE=openai_compatible
LLM_BASE_URL=https://your-provider.example/v1
LLM_API_KEY=your_api_key
LLM_MODEL=your_model_name
```

The app validates LLM configuration in `settings.py`. If `LLM_MODE=mock`, no external API key is required.

## Generate sample documents

This project ships with a fictional sample dataset. To generate the sample documents in the `documents/` folder:

```bash
python scripts/generate_sample_documents.py
```

This creates sample PDFs, DOCX, HTML, CSV, and JSON files that are intentionally fictional and not based on real legal or company data.

## Build the vectorstore

Once documents exist, build the local Chroma vector index:

```bash
python build_vectorstore.py
```

This reads all supported documents, chunks them, embeds them, and stores the results in the directory defined by `CHROMA_BASE_DIR`.

## Run the API server

Start the FastAPI app with Uvicorn:

```bash
uvicorn app:app --reload
```

Or:

```bash
python -m uvicorn app:app --reload
```

The application will run on the default FastAPI/Uvicorn port:

- http://127.0.0.1:8000

## API usage

### Health check

```bash
curl http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "ok",
  "llm_mode": "mock",
  "app_env": "development"
}
```

### Ask a question

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the liability cap in the MSA?",
    "strategy": "heading_aware"
  }'
```

Example response:

```json
{
  "answer": "...",
  "sources": ["NYAYA_MSA_Excerpt.pdf"],
  "metadata": {
    "guardrail": "passed",
    "llm_mode": "mock",
    "context_chunks": 5
  }
}
```

The `strategy` field accepts the chunking strategy configured in the project, such as `heading_aware` or other supported options defined by `chunking.py`.

## Guardrails and safety behavior

The system includes guardrails for unsupported or out-of-scope requests. The flow is implemented in `agent.py` and `context.py`.

Examples of behavior:

- out-of-scope requests are refused
- questions are answered only using the fictional sample dataset
- personal contact information is redacted before indexing or summarization

## Running tests

Run the test suite from the project root:

```bash
pytest -q
```

The tests cover:

- ingestion and document loading
- chunking logic
- redaction and PII filtering
- retrieval behavior
- guardrail handling
- API health and ask behavior

## Local-first design notes

This project is intentionally deterministic and local-first:

- it runs without requiring a production cloud service
- it uses local ChromaDB storage
- it keeps sample content fictional and safe for training/demo use
- it has a default `mock` LLM mode for running without credentials

## Troubleshooting

### `documents/` folder is missing

Run:

```bash
python scripts/generate_sample_documents.py
```

### Chroma database is empty or stale

Rebuild the vector store:

```bash
python build_vectorstore.py
```

### API fails because of missing environment values

Check the `.env` file and confirm `LLM_MODE` and any required variables are configured correctly.

### `uvicorn` command not recognized

Ensure the virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## Typical execution flow

A typical sequence for running the project is:

```bash
python -m venv .venv
source .venv/bin/activate   # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python scripts/generate_sample_documents.py
python build_vectorstore.py
uvicorn app:app --reload
```

Then send requests to:

- `GET /health`
- `POST /ask`

## Summary

Nyaya is a sample legal/compliance RAG application for local experimentation, document retrieval, and safe answer generation on fictional sources. It is structured to be easy to inspect, extend, and test while keeping the behavior deterministic and privacy-aware.
