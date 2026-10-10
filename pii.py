from __future__ import annotations

import re

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PHONE_RE = re.compile(r'(?:\+?\d[\d\s\-()]{7,}\d)')


def redact_text(text: str) -> str:
    redacted = text
    redacted = re.sub(EMAIL_RE, '[REDACTED_EMAIL]', redacted)
    redacted = re.sub(PHONE_RE, '[REDACTED_PHONE]', redacted)
    return redacted


def redact_html(html_text: str) -> str:
    return redact_text(html_text)
