from __future__ import annotations

from schemas import Chunk


def build_context(chunks: list[Chunk], max_chars: int = 6000) -> str:
    text_parts: list[str] = []
    current_chars = 0
    for chunk in chunks:
        candidate = f"Source: {chunk.source_filename}\n{chunk.text}\n"
        if current_chars + len(candidate) > max_chars:
            break
        text_parts.append(candidate)
        current_chars += len(candidate)
    return '\n---\n'.join(text_parts)


def structured_gap_guardrail(question: str) -> bool:
    lower = question.lower()
    unsupported = [
        'which company',
        'what is your name',
        'who is ceo',
        'what is the customer list',
        'sell me',
        'real legal advice',
    ]
    return any(term in lower for term in unsupported)
