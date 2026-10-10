from __future__ import annotations

import json
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from schemas import Chunk
from settings import settings


def get_client() -> chromadb.Client:
    Path(settings.chroma_base_dir).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=settings.chroma_base_dir,
        settings=ChromaSettings(anonymized_telemetry=False, allow_reset=True),
    )
    return client


def persist_chunks(chunks: list[Chunk], collection_name: str = 'nyaya_chunks') -> chromadb.Collection:
    client = get_client()
    collection = client.get_or_create_collection(name=collection_name)
    documents = [chunk.text for chunk in chunks]
    metadatas = [{**chunk.metadata, 'source_filename': chunk.source_filename, 'source_type': chunk.source_type} for chunk in chunks]
    ids = [chunk.id for chunk in chunks]
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    return collection


def query_collection(collection: chromadb.Collection, query: str, k: int = 5, where: dict | None = None):
    return collection.query(query_texts=[query], n_results=k, where=where, include=['documents', 'metadatas', 'distances'])
