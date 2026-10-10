from __future__ import annotations

import json
from pathlib import Path

from chunking import chunk_documents, fixed_size_chunks, heading_aware_chunks
from loaders import load_documents


def run_comparison(documents_dir: str | Path = 'documents') -> dict:
    documents = load_documents(documents_dir)
    heading = []
    fixed = []
    for document in documents:
        heading.extend(heading_aware_chunks(document['content'], document['filename'], document['file_type']))
        fixed.extend(fixed_size_chunks(document['content'], document['filename'], document['file_type']))
    report = {
        'heading_aware': {'count': len(heading), 'avg_chars': sum(len(chunk.text) for chunk in heading) / max(len(heading), 1)},
        'fixed_size': {'count': len(fixed), 'avg_chars': sum(len(chunk.text) for chunk in fixed) / max(len(fixed), 1)},
    }
    output_path = Path('reports/chunking_comparison.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    print(run_comparison())
