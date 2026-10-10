from __future__ import annotations

import warnings

from agent import NyayaAgent
from settings import settings

warnings.filterwarnings("ignore", category=DeprecationWarning)


QUESTIONS = [
    'What is the liability cap in the MSA?',
    'What is the quarterly compliance report deadline?',
    'What must be included in an urgent legal review request?',
    'List the open audit findings and their severity.',
]


def print_section(title: str) -> None:
    print('\n' + '=' * 80)
    print(title)
    print('=' * 80)


def _run_semantic_topk(question: str, ks: list[int]) -> None:
    agent = NyayaAgent()
    print_section(f'SEMANTIC RETRIEVAL TEST - {question}')
    for k in ks:
        print(f'\n--- top_k={k} ---')
        results = agent.fetch_semantic_matches(question, k=k)
        assert isinstance(results, list)
        if not results:
            print('No matching chunks found.')
            continue
        for index, result in enumerate(results, start=1):
            metadata = result.get('metadata') or {}
            distance = result.get('distance')
            source = metadata.get('source_filename', 'unknown')
            doc = result.get('document', '')
            preview = doc[:220].replace('\n', ' ')
            print(f'{index}. source={source}, distance={distance}')
            print(f'   preview: {preview}')


def _run_threshold_test(question: str, threshold: float) -> None:
    agent = NyayaAgent()
    print_section(f'THRESHOLD TEST - {question} (distance <= {threshold})')
    results = agent.fetch_semantic_matches(question, k=settings.retrieval_k)
    filtered = [item for item in results if item.get('distance') is not None and item.get('distance') <= threshold]
    if not filtered:
        print('No results passed the threshold filter.')
        return
    for index, result in enumerate(filtered, start=1):
        metadata = result.get('metadata') or {}
        distance = result.get('distance')
        source = metadata.get('source_filename', 'unknown')
        doc = result.get('document', '')
        preview = doc[:220].replace('\n', ' ')
        print(f'{index}. source={source}, distance={distance}')
        print(f'   preview: {preview}')


def test_semantic_retrieval_topk_variants() -> None:
    print_section('SEMANTIC RETRIEVAL COMPARISON')
    for question in QUESTIONS:
        _run_semantic_topk(question, [1, 3, 5])


def test_threshold_based_retrieval() -> None:
    print_section('THRESHOLD-BASED RETRIEVAL COMPARISON')
    for question in QUESTIONS:
        _run_threshold_test(question, settings.threshold_min_score)


def test_full_retrieval_suite() -> None:
    print_section('RETRIEVAL STRATEGY TEST SUITE')
    print(f'Configured retrieval_k={settings.retrieval_k}')
    print(f'Configured topk_min_score={settings.topk_min_score}')
    print(f'Configured threshold_min_score={settings.threshold_min_score}')
    print('Note: this project uses semantic vector retrieval via ChromaDB. The threshold check below is an approximate distance cutoff for comparison.')
    for question in QUESTIONS:
        _run_semantic_topk(question, [1, 3, 5])
        _run_threshold_test(question, settings.threshold_min_score)


if __name__ == '__main__':
    test_full_retrieval_suite()
