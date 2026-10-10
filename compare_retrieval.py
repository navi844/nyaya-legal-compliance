from __future__ import annotations

import json
from pathlib import Path

from chunking import chunk_documents
from embeddings import encode_texts
from loaders import load_documents
from retrieval import deduplicate_chunks, size_limit_context


def run_retrieval_comparison(documents_dir: str | Path = 'documents') -> dict:
    documents = load_documents(documents_dir)
    chunks = chunk_documents(documents, strategy='heading_aware')
    embeddings = encode_texts([chunk.text for chunk in chunks])
    deduped = deduplicate_chunks(chunks)
    limited = size_limit_context(deduped, 6000)
    report = {
        'before_dedup': len(chunks),
        'after_dedup': len(deduped),
        'after_context_limit': len(limited),
        'embedding_count': len(embeddings),
    }
    output_path = Path('reports/retrieval_comparison.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    print(run_retrieval_comparison())
