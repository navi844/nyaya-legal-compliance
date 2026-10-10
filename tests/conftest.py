from __future__ import annotations

from pathlib import Path

import pytest

from loaders import load_documents


@pytest.fixture(scope='session')
def documents_dir() -> Path:
    return Path(__file__).resolve().parents[1] / 'documents'


@pytest.fixture(scope='session')
def loaded_documents(documents_dir: Path):
    return load_documents(documents_dir)
