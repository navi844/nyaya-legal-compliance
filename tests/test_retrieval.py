from __future__ import annotations

from retrieval import deduplicate_chunks, size_limit_context
from chunking import chunk_document


def test_deduplicate_removes_similar_chunks(loaded_documents):
    doc = next(doc for doc in loaded_documents if doc['filename'] == 'NYAYA_MSA_Excerpt.pdf')
    chunks = chunk_document(doc, 'heading_aware')
    deduped = deduplicate_chunks(chunks)
    assert len(deduped) <= len(chunks)


def test_size_limit_works():
    chunks = [
        type('Chunk', (), {'text': 'a' * 200, 'source_filename': 'a', 'source_type': 'pdf'})(),
        type('Chunk', (), {'text': 'b' * 200, 'source_filename': 'b', 'source_type': 'pdf'})(),
    ]
    limited = size_limit_context(chunks, max_chars=250)
    assert len(limited) == 1
