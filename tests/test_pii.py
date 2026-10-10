from __future__ import annotations

from pii import redact_text


def test_redact_email_and_phone():
    sample = 'Contact Asha Verma at asha.verma@example.invalid or +91 00000 12345.'
    redacted = redact_text(sample)
    assert 'asha.verma@example.invalid' not in redacted
    assert '+91 00000 12345' not in redacted
    assert '[REDACTED_EMAIL]' in redacted
    assert '[REDACTED_PHONE]' in redacted
