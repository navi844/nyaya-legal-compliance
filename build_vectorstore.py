from __future__ import annotations

from pathlib import Path

from chunking import chunk_documents
from embeddings import encode_texts
from loaders import load_documents
from settings import settings
from vectorstore import persist_chunks


def build_vectorstore(documents_dir: str | Path = 'documents', strategy: str | None = None) -> None:
    documents = load_documents(documents_dir)
    chunks = chunk_documents(documents, strategy or settings.chunking_strategy)
    embeddings = encode_texts([chunk.text for chunk in chunks])
    for chunk, vector in zip(chunks, embeddings):
        chunk.metadata['embedding'] = vector
    persist_chunks(chunks)


if __name__ == '__main__':
    build_vectorstore()
    print('Vector store built successfully.')
