from __future__ import annotations


def grounded_answer_prompt(question: str, context: str) -> str:
    return f'''
You are a legal compliance assistant for fictional sample data only.
Answer using ONLY the information in the provided context.
If the answer cannot be supported by the context, say so.
Do not invent facts or legal advice.
Question: {question}
Context:
{context}
Return a concise answer with a list of cited source filenames.
'''.strip()


def mock_answer(question: str, context: str) -> str:
    if 'liability' in question.lower() and 'fees paid or payable' in context.lower():
        return 'The aggregate liability cap equals fees paid or payable under the applicable Order Form during the 12 months preceding the claim event. Source: NYAYA_MSA_Excerpt.pdf.'
    if 'quarterly compliance report' in question.lower() or 'deadline' in question.lower() and '15th' in context:
        return 'The quarterly compliance report is due on the 15th calendar day after each quarter ends; if that date falls on a public holiday, the due date moves to the next business day. Source: NYAYA_Regulatory_Compliance_Circular.docx.'
    if 'urgent' in question.lower():
        return 'Urgent review requires an Urgent Legal Review form and contact with the fictional duty counsel; the request must include customer name, contract value band, required signature date, risk summary, and account owner. Source: NYAYA_Legal_FAQ.html.'
    if 'open' in question.lower() and 'audit' in question.lower():
        return 'Open audit findings include privileged-access review evidence incomplete, vendor due-diligence renewal overdue, retention exception lacks documented approval, and incident exercise action owner not assigned. Source: NYAYA_Compliance_Audit_Log.csv.'
    if 'filing' in question.lower() and 'due' in question.lower():
        return 'Due or overdue filings on 2026-10-10 include FIL-2026-101, FIL-2026-102, and FIL-2026-105. Source: NYAYA_Regulatory_Filing_Tracker.json.'
    return 'The context supports a factual answer, but a direct match was not found in the provided local sample data. Please ask a question grounded in the sample documents. Source: NYAYA_MSA_Excerpt.pdf.'
