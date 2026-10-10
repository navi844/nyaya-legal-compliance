from __future__ import annotations

from chunking import chunk_document, fixed_size_chunks, heading_aware_chunks


def test_heading_aware_chunking_has_sections(loaded_documents):
    document = next(doc for doc in loaded_documents if doc['filename'] == 'NYAYA_MSA_Excerpt.pdf')
    chunks = chunk_document(document, 'heading_aware')
    assert len(chunks) >= 2
    assert any('Section 8' in chunk.text for chunk in chunks)


def test_fixed_size_chunking_returns_chunks():
    text = 'This is a long passage. ' * 50
    chunks = fixed_size_chunks(text, 'sample.txt', 'text')
    assert len(chunks) >= 1
    assert all(len(chunk.text) > 0 for chunk in chunks)
