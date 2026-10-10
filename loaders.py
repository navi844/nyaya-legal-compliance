from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable

import fitz
from bs4 import BeautifulSoup
from docx import Document

from pii import redact_text


def _metadata_from_text(content: str) -> dict[str, str]:
    metadata = {}
    for line in content.splitlines():
        if ':' in line and 'Document ID' in line:
            metadata['document_id'] = line.split(':', 1)[1].strip()
        elif ':' in line and 'Version' in line:
            metadata['version'] = line.split(':', 1)[1].strip()
        elif ':' in line and 'Effective Date' in line:
            metadata['effective_date'] = line.split(':', 1)[1].strip()
        elif ':' in line and 'Classification' in line:
            metadata['classification'] = line.split(':', 1)[1].strip()
    return metadata


def load_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    pages = [page.get_text('text', sort=True) for page in doc]
    text = '\n'.join(pages)
    return redact_text(text)


def load_docx(path: Path) -> str:
    doc = Document(str(path))
    paragraphs = [p.text for p in doc.paragraphs]
    return redact_text('\n'.join(paragraphs))


def load_html(path: Path) -> str:
    html = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text('\n', strip=True)
    return redact_text(text)


def load_csv(path: Path) -> str:
    rows: list[str] = []
    with path.open('r', newline='', encoding='utf-8') as handle:
        for raw in handle:
            if raw.strip().startswith('#'):
                continue
            if raw.strip().startswith('Document ID') or raw.strip().startswith('Version') or raw.strip().startswith('Effective Date'):
                rows.append(raw.strip())
                continue
            rows.append(raw.strip())
    return redact_text('\n'.join(rows))


def load_json(path: Path) -> str:
    payload = json.loads(path.read_text(encoding='utf-8'))
    flattened = []
    for key, value in payload.items():
        if isinstance(value, dict):
            flattened.append(f'{key}: {json.dumps(value, sort_keys=True)}')
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    flattened.append(json.dumps(item, sort_keys=True))
                else:
                    flattened.append(str(item))
        else:
            flattened.append(f'{key}: {value}')
    return redact_text('\n'.join(flattened))


def render_csv_rows(path: Path) -> list[dict[str, str]]:
    rows = []
    with path.open('r', newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({k: (v or '').strip() for k, v in row.items()})
    return rows


def load_documents(documents_dir: str | Path) -> list[dict]:
    directory = Path(documents_dir)
    items: list[dict] = []
    for file_path in sorted(directory.iterdir()):
        if not file_path.is_file():
            continue
        suffix = file_path.suffix.lower()
        if suffix == '.pdf':
            text = load_pdf(file_path)
            file_type = 'pdf'
        elif suffix == '.docx':
            text = load_docx(file_path)
            file_type = 'docx'
        elif suffix == '.html':
            text = load_html(file_path)
            file_type = 'html'
        elif suffix == '.csv':
            text = load_csv(file_path)
            file_type = 'csv'
        elif suffix == '.json':
            text = load_json(file_path)
            file_type = 'json'
        else:
            continue
        items.append({
            'filename': file_path.name,
            'file_type': file_type,
            'original_path': str(file_path.resolve()),
            'content': text,
            'metadata': _metadata_from_text(text),
        })
    return items
