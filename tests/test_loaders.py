from __future__ import annotations

from pathlib import Path


def test_load_documents_count(loaded_documents):
    assert len(loaded_documents) == 5


def test_document_metadata_present(loaded_documents):
    filenames = {doc['filename'] for doc in loaded_documents}
    assert 'NYAYA_MSA_Excerpt.pdf' in filenames
    assert 'NYAYA_Regulatory_Compliance_Circular.docx' in filenames
    assert 'NYAYA_Legal_FAQ.html' in filenames
    assert 'NYAYA_Compliance_Audit_Log.csv' in filenames
    assert 'NYAYA_Regulatory_Filing_Tracker.json' in filenames


def test_html_redaction_in_document(loaded_documents):
    faq_doc = next(doc for doc in loaded_documents if doc['filename'] == 'NYAYA_Legal_FAQ.html')
    assert 'asha.verma@example.invalid' not in faq_doc['content']
    assert '+91 00000 12345' not in faq_doc['content']
