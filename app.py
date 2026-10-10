from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import NyayaAgent
from settings import settings

app = FastAPI(title='Nyaya Legal & Compliance RAG API')
agent = NyayaAgent(documents_dir='documents')


class QueryPayload(BaseModel):
    question: str
    strategy: str = 'heading_aware'


@app.get('/health')
def health() -> dict:
    return {'status': 'ok', 'llm_mode': settings.llm_mode, 'app_env': settings.app_env}


@app.post('/ask')
def ask(payload: QueryPayload) -> dict:
    try:
        result = agent.answer_question(payload.question, strategy=payload.strategy)
        return {
            'answer': result.answer,
            'sources': result.sources,
            'metadata': result.metadata,
        }
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
