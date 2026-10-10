# Nyaya Legal & Compliance RAG Project

Nyaya is a local-first, deterministic retrieval-augmented generation (RAG) project for fictional legal and compliance review workflows. It ingests sample legal and compliance documents, redacts personally identifiable information (PII), chunks the content, embeds it, stores embeddings in a local Chroma database, and answers grounded questions using a mock LLM or an OpenAI-compatible backend.

The project is designed for offline experimentation and demo-friendly testing. All sample content is fictional and safe for training or demonstration purposes.

## Project goals

- Ingest legal and compliance files in PDF, DOCX, HTML, CSV, and JSON formats
- Remove PII before indexing and retrieval
- Build retrieval-friendly chunks using different chunking strategies
- Embed and store chunks locally in ChromaDB
- Retrieve the most relevant context for a question
- Enforce guardrails for out-of-scope or unsupported requests
- Expose the system through a FastAPI API
- Provide a test suite that covers ingestion, chunking, retrieval, PII redaction, and guardrail behavior

## High-level architecture

The application is structured as a simple, local-first RAG pipeline:

1. Documents are loaded from the `documents/` directory via `loaders.py`
2. Content is cleaned and PII-redacted via `pii.py`
3. Text is split into chunks using strategies in `chunking.py`
4. Chunks are embedded using `embeddings.py`
5. Embeddings are persisted to the local Chroma database using `vectorstore.py`
6. A question is processed by `agent.py`
7. Relevant chunks are retrieved from the Chroma index
8. A limited context is assembled and passed to the LLM client
9. A final answer is returned with source metadata and guardrail status
10. The FastAPI service exposes the workflow through `app.py`

## Main project files

- `app.py` – FastAPI endpoints for health and question answering
- `agent.py` – orchestration for indexing, retrieval, guardrails, and predefined test scenarios
- `settings.py` – environment-based configuration and validation
- `loaders.py` – document ingestion for PDF, DOCX, HTML, CSV, and JSON files
- `chunking.py` – chunking logic for heading-aware and fixed-size segmentation
- `embeddings.py` – sentence embedding generation
- `vectorstore.py` – ChromaDB client and persistent collection setup
- `retrieval.py` – deduplication and context-size filtering
- `context.py` – context assembly and unsupported-question guardrail logic
- `llm_client.py` – mock or OpenAI-compatible LLM integration
- `pii.py` – email and phone redaction logic
- `build_vectorstore.py` – builds the local vector database
- `scripts/generate_sample_documents.py` – generates fictional sample documents
- `tests/` – coverage for ingestion, PII, retrieval, guardrails, and API behavior

## File and data flow

The project uses a deterministic and local-first pipeline:

- Sample documents are created in `documents/`
- `loaders.py` reads each file and returns structured document metadata
- `pii.py` redacts PII before documents are stored or indexed
- `chunking.py` creates chunks based on either heading-aware segmentation or fixed-size chunk splitting
- `embeddings.py` maps chunk text to embeddings
- `vectorstore.py` creates or updates the persisted Chroma collection
- `agent.py` builds answers from the retrieved context and returns metadata
- `app.py` exposes the same functionality over HTTP

## Requirements

- Python 3.10+
- pip
- Virtual environment support
- Internet access only for dependency installation or real OpenAI access

## Dependency installation

From the project root, create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment configuration

The project loads settings from `.env` using `settings.py`.

Example `.env`:

```env
APP_ENV=development
CHROMA_BASE_DIR=./chroma_db
CHUNKING_STRATEGY=heading_aware
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODE=mock
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
MAX_CONTEXT_CHARS=6000
RETRIEVAL_K=5
TOPK_MIN_SCORE=0.30
THRESHOLD_MIN_SCORE=0.45
NEAR_DUPLICATE_THRESHOLD=0.90
REFERENCE_DATE=2026-10-10
```

Notes:

- `LLM_MODE=mock` is the default and does not require external credentials
- The project supports an OpenAI-compatible backend via `OPENAI_API_KEY`, `OPENAI_MODEL`, and `OPENAI_EMBEDDING_MODEL`
- Legacy `LLM_*` values are also supported for compatibility

## Sample document generation

The project includes fictional sample documents to keep testing safe and deterministic.

Generate sample files:

```bash
python scripts/generate_sample_documents.py
```

This creates document files under `documents/`, including:

- `NYAYA_MSA_Excerpt.pdf`
- `NYAYA_Regulatory_Compliance_Circular.docx`
- `NYAYA_Legal_FAQ.html`
- `NYAYA_Compliance_Audit_Log.csv`
- `NYAYA_Regulatory_Filing_Tracker.json`

These documents contain fictional legal/compliance scenarios and are not based on real company or legal data.

## Chunking process

Chunking is implemented in `chunking.py`.

### heading_aware

This is the default strategy.

- Splits text by headings and section markers such as `Section`, numbered headings, HTML headings, and document metadata markers
- Preserves logical document structure
- Works well for legal and compliance content where sections matter

### fixed_size

This strategy uses paragraph-based chunking with a fixed character limit and overlap.

- Useful for comparison testing against heading-aware segmentation
- Helps evaluate how retrieval behaves with different chunk boundaries

Example:

```bash
python build_vectorstore.py --strategy fixed
```

The selected strategy is used in `build_vectorstore.py`, which resolves the CLI choice before indexing.

## Retrieval process

Retrieval in this project is based on a semantic vector search over a local ChromaDB collection.

### Semantic retrieval

The main retrieval mechanism is:

- embed the user question
- query ChromaDB for nearby text chunks
- fetch the top-k results
- sort or filter based on score and distance
- reduce the list to the context budget

Relevant files:

- `agent.py` – `NyayaAgent.fetch_semantic_matches()`
- `vectorstore.py` – Chroma collection query logic
- `settings.py` – retrieval parameters
- `retrieval.py` – deduplication and limit logic

### Retrieval settings

The project uses parameters defined in `settings.py`:

- `RETRIEVAL_K=5`
- `TOPK_MIN_SCORE=0.30`
- `THRESHOLD_MIN_SCORE=0.45`
- `NEAR_DUPLICATE_THRESHOLD=0.90`
- `MAX_CONTEXT_CHARS=6000`

These values influence:

- how many chunks are returned
- how strict the filtering is
- how much text is kept for forming context
- whether similar chunks are removed before the final answer is generated

## Vector database build

Build the local Chroma index:

```bash
python build_vectorstore.py
```

Or with a selected chunking strategy:

```bash
python build_vectorstore.py --strategy fixed
```

The script prints a summary that includes:

- database directory
- collection name
- chunking strategy
- number of documents processed
- number of chunks created
- embeddings generated
- collection size
- elapsed time

The default database directory is `./chroma_db`.

## Running the API

Start the API server:

```bash
python -m uvicorn app:app --reload
```

Or:

```bash
uvicorn app:app --reload
```

The app runs on:

- http://127.0.0.1:8000

Swagger docs are available at:

- http://127.0.0.1:8000/docs

## API usage

### Health check

```bash
curl http://127.0.0.1:8000/health
```

Expected example response:

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

## Agent testing

The project includes predefined testing questions in `agent.py` that demonstrate both grounded retrieval behavior and guardrail behavior.

Run:

```bash
python agent.py
```

This prints scenario results for questions such as:

- liability cap in the MSA
- indemnification obligations
- compliance reporting deadline and penalty
- audit findings and severity
- urgent legal review requested documents
- unsupported customer-list question that triggers the guardrail

This is useful for manual validation of the retrieval-answer pipeline.

## PII redaction testing

The project intentionally includes a fictional email and phone number in the HTML FAQ sample.

Source file:

- `scripts/generate_sample_documents.py`
- `documents/NYAYA_Legal_FAQ.html`

Direct redaction test:

```bash
python -c "from pii import redact_text; text='Fictional email: asha.verma@example.invalid | phone: +91 00000 12345'; print(redact_text(text))"
```

Expected output contains:

- `[REDACTED_EMAIL]`
- `[REDACTED_PHONE]`

Document-level check:

```bash
python -c "from loaders import load_documents; docs = load_documents('documents'); faq = next(d for d in docs if d['filename']=='NYAYA_Legal_FAQ.html'); print('EMAIL_PRESENT=', 'asha.verma@example.invalid' in faq['content']); print('EMAIL_REDACTED=', '[REDACTED_EMAIL]' in faq['content']); print('PHONE_REDACTED=', '[REDACTED_PHONE]' in faq['content'])"
```

## Retrieval strategy testing

A retrieval strategy test file is included under `tests/`.

Run:

```bash
python -m pytest tests/test_retrieval_strategies.py -q -s
```

This shows:

- semantic retrieval with different `top_k` values
- threshold-based filtering comparison
- multiple representative legal/compliance questions

This helps compare the behavior of retrieval at different sizes and score cutoffs.

## Guardrails and safety behavior

The guardrail logic resides in `context.py` and is enforced in `agent.py`.

Examples of blocked questions include:

- real customer list queries
- unrelated business questions not grounded in the sample dataset
- requests for real legal advice
- unsupported requests that are not covered by the fictional legal/compliance corpus

Guardrail response example:

```text
I can only answer questions grounded in the fictional Nyaya sample documents and I cannot support that request.
```

## Testing coverage

The test suite covers the main project guarantees:

- document loading and ingestion (`tests/test_loaders.py`)
- chunking logic (`tests/test_chunking.py`)
- retrieval behavior (`tests/test_retrieval.py`, `tests/test_retrieval_strategies.py`)
- PII redaction (`tests/test_pii.py`)
- guardrail logic (`tests/test_guardrail.py`)
- API health and ask behavior (`tests/test_api.py`)
- context and prompt assembly (`tests/test_context.py`)

Run all tests:

```bash
pytest -q
```

Or focus on retrieval testing:

```bash
python -m pytest tests/test_retrieval_strategies.py -q -s
```

## Practical execution order

A typical full run goes like this:

```bash
python -m venv .venv
source .venv/bin/activate   # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python scripts/generate_sample_documents.py
python build_vectorstore.py
python -m uvicorn app:app --reload
```

Then verify directly:

- `GET /health`
- `POST /ask`
- `python agent.py`
- `python -m pytest tests/test_retrieval_strategies.py -q -s`

## Troubleshooting

### Missing sample documents

```bash
python scripts/generate_sample_documents.py
```

### Empty or stale Chroma index

```bash
python build_vectorstore.py
```

### Wrong chunking strategy used

Check `settings.py` and pass the strategy explicitly:

```bash
python build_vectorstore.py --strategy fixed
```

### API not starting

Ensure the environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### LLM config issues

Check `.env` and verify one of these is configured:

- `LLM_MODE=mock`
- or `LLM_MODE=openai_compatible` with valid OpenAI values

## Summary

Nyaya is a fictional legal/compliance RAG project that demonstrates a complete local-first workflow: document ingestion, PII wiping, chunking, embedding, semantic retrieval, guardrails, and API-based answer generation. It is designed for clear experimentation, easy debugging, and assignment-friendly testing across retrieval, chunking, and safety scenarios.
