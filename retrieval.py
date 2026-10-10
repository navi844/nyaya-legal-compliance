from __future__ import annotations

from typing import Iterable

from schemas import Chunk, QueryResult


def deduplicate_chunks(chunks: Iterable[Chunk], threshold: float = 0.90) -> list[Chunk]:
    deduped: list[Chunk] = []
    seen: list[str] = []
    for chunk in chunks:
        if any(_similar(chunk.text, existing.text, threshold) for existing in seen):
            continue
        deduped.append(chunk)
        seen.append(chunk)
    return deduped


def _similar(left: str, right: str, threshold: float) -> bool:
    left_norm = left.lower().strip()
    right_norm = right.lower().strip()
    if left_norm == right_norm:
        return True
    if not left_norm or not right_norm:
        return False
    same = 0
    for idx in range(min(len(left_norm), len(right_norm))):
        if left_norm[idx] == right_norm[idx]:
            same += 1
    similarity = same / max(len(left_norm), len(right_norm))
    return similarity >= threshold


def size_limit_context(chunks: Iterable[Chunk], max_chars: int = 6000) -> list[Chunk]:
    selected: list[Chunk] = []
    total = 0
    for chunk in chunks:
        if total + len(chunk.text) > max_chars:
            continue
        selected.append(chunk)
        total += len(chunk.text)
    return selected


def rank_and_filter(results: list[QueryResult], min_score: float = 0.30) -> list[QueryResult]:
    filtered = [item for item in results if item.score >= min_score]
    return sorted(filtered, key=lambda item: item.score, reverse=True)


def fetch_topk_by_scores(chunks: list[Chunk], query: str, scores: list[float], k: int = 5) -> list[QueryResult]:
    scored = [QueryResult(chunk=chunk, score=score) for chunk, score in zip(chunks, scores)]
    return rank_and_filter(scored, min_score=0.0)[:k]
