from __future__ import annotations

import argparse
import time
from pathlib import Path

from chunking import chunk_documents
from embeddings import encode_texts
from loaders import load_documents
from settings import settings
from vectorstore import persist_chunks


def resolve_strategy(value: str | None) -> str:
    if value is None:
        return settings.chunking_strategy
    normalized = value.strip().lower()
    aliases = {
        'fixed': 'fixed_size',
        'fixed_size': 'fixed_size',
        'heading': 'heading_aware',
        'heading_aware': 'heading_aware',
    }
    return aliases.get(normalized, value)


def build_vectorstore(documents_dir: str | Path = 'documents', strategy: str | None = None) -> dict:
    chosen_strategy = resolve_strategy(strategy)
    start_time = time.perf_counter()
    documents = load_documents(documents_dir)
    document_count = len(documents)

    chunks = chunk_documents(documents, chosen_strategy)
    chunk_count = len(chunks)

    embeddings = encode_texts([chunk.text for chunk in chunks])
    for chunk, vector in zip(chunks, embeddings):
        chunk.metadata['embedding'] = vector

    collection = persist_chunks(chunks)
    elapsed_time = time.perf_counter() - start_time

    summary = {
        'database_dir': str(settings.chroma_dir),
        'collection_name': 'nyaya_chunks',
        'strategy': chosen_strategy,
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
    parser = argparse.ArgumentParser(description='Build the Nyaya Chroma vector database.')
    parser.add_argument('--strategy', choices=['heading_aware', 'fixed_size', 'fixed', 'heading'], default=None,
                        help='Chunking strategy to use: heading_aware or fixed_size (fixed is accepted as alias).')
    args = parser.parse_args()

    build_vectorstore(strategy=args.strategy)
    print('Vector store built successfully.')
