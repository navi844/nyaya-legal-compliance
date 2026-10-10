from __future__ import annotations

from context import structured_gap_guardrail


def test_guardrail_rejects_unspecified_company_questions():
    assert structured_gap_guardrail('Who are your customers?') is True
