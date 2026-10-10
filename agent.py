from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from chunking import chunk_documents
from context import build_context, structured_gap_guardrail
from embeddings import encode_texts
from llm_client import LLMClient
from loaders import load_documents
from retrieval import deduplicate_chunks, size_limit_context
from settings import settings
from vectorstore import get_client, persist_chunks


@dataclass
class AgentAnswer:
    answer: str
    sources: list[str]
    metadata: dict


class NyayaAgent:
    def __init__(self, documents_dir: str | Path = 'documents', llm_mode: str | None = None):
        self.documents_dir = documents_dir
        self.llm = LLMClient(mode=llm_mode or settings.llm_mode)

    def build_index(self, strategy: str | None = None) -> list[str]:
        documents = load_documents(self.documents_dir)
        chunks = chunk_documents(documents, strategy or settings.chunking_strategy)
        embeddings = encode_texts([chunk.text for chunk in chunks])
        for chunk, vector in zip(chunks, embeddings):
            chunk.metadata['embedding'] = vector
        self.collection = persist_chunks(chunks)
        return [chunk.id for chunk in chunks]

    def answer_question(self, question: str, strategy: str | None = None) -> AgentAnswer:
        if structured_gap_guardrail(question):
            return AgentAnswer(
                answer='I can only answer questions grounded in the fictional Nyaya sample documents and I cannot support that request.',
                sources=[],
                metadata={'guardrail': 'unsupported_question', 'llm_mode': self.llm.mode_label},
            )

        documents = load_documents(self.documents_dir)
        chunks = chunk_documents(documents, strategy or settings.chunking_strategy)
        deduped = deduplicate_chunks(chunks, threshold=settings.near_duplicate_threshold)
        limited = size_limit_context(deduped, max_chars=settings.max_context_chars)
        context = build_context(limited, settings.max_context_chars)
        answer = self.llm.generate(question, context)
        sources = sorted({chunk.source_filename for chunk in limited})
        return AgentAnswer(
            answer=answer,
            sources=sources,
            metadata={'guardrail': 'passed', 'llm_mode': self.llm.mode_label, 'context_chunks': len(limited)},
        )

    def fetch_semantic_matches(self, question: str, k: int | None = None) -> list[dict]:
        collection = get_client().get_collection(name='nyaya_chunks')
        query = collection.query(query_texts=[question], n_results=k or settings.retrieval_k, include=['documents', 'metadatas', 'distances'])
        results = []
        for doc, meta, dist in zip(query['documents'][0], query['metadatas'][0], query['distances'][0]):
            results.append({'document': doc, 'metadata': meta, 'distance': dist})
        return results
