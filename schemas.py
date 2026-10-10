from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceDocument:
    filename: str
    file_type: str
    original_path: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    id: str
    text: str
    source_filename: str
    source_type: str
    metadata: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0


@dataclass
class QueryResult:
    chunk: Chunk
    score: float


@dataclass
class AskRequest:
    question: str
    strategy: str = 'heading_aware'


@dataclass
class AskResponse:
    answer: str
    sources: list[str]
    metadata: dict[str, Any]
