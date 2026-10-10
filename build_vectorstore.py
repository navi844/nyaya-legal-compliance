from __future__ import annotations

import time
from pathlib import Path

from chunking import chunk_documents
from embeddings import encode_texts
from loaders import load_documents
from settings import settings
from vectorstore import persist_chunks


def build_vectorstore(documents_dir: str | Path = 'documents', strategy: str | None = None) -> dict:
    start_time = time.perf_counter()
    documents = load_documents(documents_dir)
    document_count = len(documents)

    chunks = chunk_documents(documents, strategy or settings.chunking_strategy)
    chunk_count = len(chunks)

    embeddings = encode_texts([chunk.text for chunk in chunks])
    for chunk, vector in zip(chunks, embeddings):
        chunk.metadata['embedding'] = vector

    collection = persist_chunks(chunks)
    elapsed_time = time.perf_counter() - start_time

    summary = {
        'database_dir': str(settings.chroma_dir),
        'collection_name': 'nyaya_chunks',
        'strategy': strategy or settings.chunking_strategy,
        'documents_processed': document_count,
        'chunks_created': chunk_count,
        'embedding_count': len(embeddings),
        'collection_size': collection.count(),
        'elapsed_seconds': round(elapsed_time, 3),
    }

    print('Chroma DB build summary:')
    print(f"- Database directory: {summary['database_dir']}")
    print(f"- Collection name: {summary['collection_name']}")
    print(f"- Chunking strategy: {summary['strategy']}")
    print(f"- Documents processed: {summary['documents_processed']}")
    print(f"- Chunks created: {summary['chunks_created']}")
    print(f"- Embeddings generated: {summary['embedding_count']}")
    print(f"- Collection size: {summary['collection_size']}")
    print(f"- Total time: {summary['elapsed_seconds']} seconds")
    return summary


if __name__ == '__main__':
    build_vectorstore()
    print('Vector store built successfully.')
