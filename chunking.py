from __future__ import annotations

import re
from typing import Iterable

from schemas import Chunk


def heading_aware_chunks(text: str, source_filename: str, source_type: str) -> list[Chunk]:
    normalized = text.replace('\r\n', '\n')
    sections = re.split(r'\n(?=(?:Section|\d+\s*[-–]|<h[1-6]>|Audit ID|filing_id|Document ID))', normalized)
    chunks: list[Chunk] = []
    for index, section in enumerate(section for section in sections if section.strip()):
        chunk_text = section.strip()
        if not chunk_text:
            continue
        chunks.append(Chunk(
            id=f'{source_filename}:{index}',
            text=chunk_text,
            source_filename=source_filename,
            source_type=source_type,
            metadata={'strategy': 'heading_aware'},
        ))
    return chunks


def fixed_size_chunks(text: str, source_filename: str, source_type: str, size: int = 500, overlap: int = 80) -> list[Chunk]:
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n+', text) if p.strip()]
    chunks: list[Chunk] = []
    current: list[str] = []
    current_chars = 0
    for paragraph in paragraphs:
        paragraph_chars = len(paragraph)
        if current and current_chars + paragraph_chars > size:
            joined = ' '.join(current)
            chunks.append(Chunk(
                id=f'{source_filename}:{len(chunks)}',
                text=joined,
                source_filename=source_filename,
                source_type=source_type,
                metadata={'strategy': 'fixed_size'},
            ))
            current = [paragraph[-overlap:]] if overlap < len(paragraph) else [paragraph]
            current_chars = len(current[0])
            continue
        current.append(paragraph)
        current_chars += paragraph_chars
    if current:
        chunks.append(Chunk(
            id=f'{source_filename}:{len(chunks)}',
            text=' '.join(current),
            source_filename=source_filename,
            source_type=source_type,
            metadata={'strategy': 'fixed_size'},
        ))
    return chunks


def chunk_document(document: dict, strategy: str | None = None) -> list[Chunk]:
    strategy_name = strategy or 'heading_aware'
    if strategy_name == 'fixed_size':
        return fixed_size_chunks(document['content'], document['filename'], document['file_type'])
    return heading_aware_chunks(document['content'], document['filename'], document['file_type'])


def chunk_documents(documents: Iterable[dict], strategy: str | None = None) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        chunks.extend(chunk_document(doc, strategy))
    return chunks
