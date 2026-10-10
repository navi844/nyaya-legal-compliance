from __future__ import annotations

from context import build_context, structured_gap_guardrail


def test_build_context_truncates():
    chunks = [
        type('Chunk', (), {'text': 'A' * 100, 'source_filename': 'one'})(),
        type('Chunk', (), {'text': 'B' * 100, 'source_filename': 'two'})(),
    ]
    context = build_context(chunks, max_chars=150)
    assert len(context) <= 150


def test_guardrail_blocks_unsupported_questions():
    assert structured_gap_guardrail('What is the CEO of the company?')
